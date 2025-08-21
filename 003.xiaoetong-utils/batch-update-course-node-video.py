import requests
import os

# 根据课程小节标题，批量更新小节关联视频

# 需要先填充以下信息
cookie = """"""
if cookie is None or len(cookie) == 0 :
    raise Exception('Cookie 不能为空')

courseId = ''
if courseId is None or len(courseId) == 0:
    raise Exception('课程 ID 不能为空')

# 1. 获取课程章节列表
chapterDetailUrl = 'https://admin.xiaoe-tech.com/xe.course.b_admin_r.camp_pro.chapter.list.get/1.0.0'
chapterDetails = []
chapters = []
page = 1
while True:
    payload = {
        "course_id": courseId,
        "sub_course_id":"",
        "p_id":"",
        "page":page,
        "page_size":50,
        "search_word":""
    }
    headers = {
        'Cookie': cookie
    }
    response = requests.post(chapterDetailUrl, headers = headers, json = payload).json()
    if response['code'] != 0:
        raise Exception('获取课程章节列表失败')
    data = response['data']
    # chapterDetails += data['list']
    for item in data['list']:
        if item['chapter_type'] == 1:
            chapters.append(item)
        elif item['chapter_type'] == 2:
            chapterDetails.append(item)
    total = data['total']
    totalPage = total / 50 + 1
    if page >= totalPage:
        break
    page += 1

# 1.1 提取章节中的小节
for chapter in chapters:
    page = 1
    while True:
        payload = {
            "course_id": courseId,
            "sub_course_id":"",
            "p_id": chapter['chapter_id'],
            "page":page,
            "page_size":50,
            "search_word":""
        }
        headers = {
            'Cookie': cookie
        }
        response = requests.post(chapterDetailUrl, headers = headers, json = payload).json()
        if response['code'] != 0:
            raise Exception('获取课程章节列表失败')
        data = response['data']
        chapterDetails += data['list']
        total = data['total']
        totalPage = total / 50 + 1
        if page >= totalPage:
            break
        page += 1

print('chapterDetails count: ' + str(len(chapterDetails)))

# 2. 依次处理各个小节
headers = {
    'Cookie': cookie
}

for chapterDetail in chapterDetails:
    # 2.1 获取小节标题
    originTitle = chapterDetail['chapter_title']
    chapterId = chapterDetail['chapter_id']

    # 2.2 查询小节视频详情，如果小节的视频文件标题包含小节标题，说明已经关联了视频，跳过
    videoFileUrl = 'https://admin.xiaoe-tech.com/xe.course.b_admin_r.video.info.get/1.0.0?resource_id=' + chapterId
    videoFileInfo = requests.get(videoFileUrl, headers = headers).json()
    if videoFileInfo['code'] != 0:
        print('%s: 获取视频文件信息失败' % originTitle)
        continue

    originVideoFileName = videoFileInfo['data']['file_name']
    if originVideoFileName.find(originTitle) != -1:
        print('%s: 已经关联视频，跳过' % originTitle)
        continue

    # 2.3 根据小节标题搜索视频，如果能匹配到唯一结果，则更新小节视频，如果不能，则输出并跳过
    marterialSearchUrl = 'https://admin.xiaoe-tech.com/xe.material-center.access.list/1.0.0'
    tmpHeaders = {
        'Cookie': cookie,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = [
        ('type', 3),
        ('page', 1),
        ('page_size', 10),
        ('keyword', originTitle),
        ('query_type', 4),
        ('order_by', 5),
        ('order_by_type', 1)
    ]
    response = requests.post(marterialSearchUrl, headers = tmpHeaders, data = data)
    if response.json()['code'] != 0:
        raise Exception('%s: 搜索视频失败' % originTitle)
    data = response.json()['data']
    resources = data['list']
    total = data['total']
    if total == 0:
        print('%s: 没有找到视频' % originTitle)
        continue
    elif total >= 1:
        # 如果找到一个或多个视频，根据标题进行完全匹配，只有有且仅有一个完全匹配，认为有效
        # 否则，输出并跳过
        resources = [resource for resource in resources if os.path.splitext(resource['title'])[0] == originTitle]
        if len(resources) == 0:
            print('%s: 找到多个视频，但无法精确匹配' % originTitle)
            continue
        elif len(resources) > 1:
            print('%s: 精确匹配到多个视频，需要手动处理' % originTitle)
            continue
    resource = resources[0]
    imgUrl = resource['material_property']['patch_img_url']
    fileId = resource['material_property']['file_id']
    fileName = resource['title']
    videoUrl = resource['url']
    videoLength = resource['material_property']['length']
    videoSize = resource['material_size']

    # 2.3 更新小节视频
    payload = {
        "content": {
            "cover_img_url": imgUrl,
            "file_id": fileId,
            "file_name": fileName,
            "patch_img_url": imgUrl,
            "video_length": videoLength,
            "video_size": videoSize,
            "video_url": videoUrl
        },
        "course": {
            "descrb": "",
            "img_url": imgUrl,
            "learn_page_cover": imgUrl,
            "title": originTitle
        },
        "resource_id": chapterId,
        "review_parent_ids": [
            {
                "resource_id": courseId,
                "resource_type": 50,
                "sub_course_id": ""
            }
        ]
    }

    updateVideoUrl = 'https://admin.xiaoe-tech.com/xe.course.b_admin_w.video.update/1.0.0'
    updateVideoResponse = requests.post(updateVideoUrl, headers = headers, json = payload)
    # print(updateVideoResponse.json())
    if updateVideoResponse.json()['code'] != 0:
        print('%s: 更新视频失败' % originTitle)
        continue
    print('%s: 更新视频成功' % originTitle)