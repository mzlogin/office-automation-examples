import requests

# 本脚本的应用场景是在「视频」列表里，通过一定的条件搜索出一系列的视频，然后将这些视频按照一定的规则排序后，依次更新这些视频的所属课程和售卖设置

# 需要先填充 cookie、resourceIds、parentId、parentType、fetchSortedResourceIds 函数里的 data 搜索条件再运行

cookie = """"""
parentId = ''
parentType = 50

def fetchSortedResourceIds():
    searchVideoUrl = 'https://admin.xiaoe-tech.com/xe.course.b_admin_r.course.base.list/1.0.0'
    headers = {
        'Cookie': cookie,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    resources = []
    page = 1
    while True:
        data = [
            ('search_content', ), # fill param
            ('resource_type', 3),
            ('sale_status', -1),
            ('created_source', 1),
            ('auth_type', -1),
            ('page_index', page),
            ('page_size', 50),
            ('tags[0]', ) # fill param
        ]
        response = requests.post(searchVideoUrl, headers = headers, data = data)
        # print(response.json())
        if response.json()['code'] != 0:
            raise Exception('fetchSortedResourceIds 失败')
        data = response.json()['data']
        resources += data['list']
        total = data['total']
        totalPage = total / 50 + 1
        if page >= totalPage:
            break
        page += 1
    print('resources count: ' + str(len(resources)))
    # 将 resources 排序，根据 title 排序，title 的格式示例：
    # 初二秋季第8讲例3、初二春季第18讲例14
    # 含有 '秋' 的排在含有 '春' 的前面，title 里都可以解析出两个数，这两个数可能是一位数也可能是两位数，按这两个数的大小排序
    resources.sort(key = lambda x: (x['title'].find('春'), int(x['title'].split('第')[1].split('讲')[0]), int(x['title'].split('例')[1])))

    # resourceTitles = [resource['title'] for resource in resources]
    # for title in resourceTitles:
    #     print(title)

    return [resource['resource_id'] for resource in resources]

# resourceIds，过滤 https://admin.xiaoe-tech.com/xe.course.b_admin_r.course.base.list/1.0.0 请求所得
# 倒序，因为视频是按照倒序的顺序添加的
# resourceIds = [ ]
# resourceIds.reverse()

resourceIds = fetchSortedResourceIds()

def updateVideoParentAndSalesSettings(resourceId, parentId, parentType):
    print('Updating video: ' + resourceId)
    # 1. 获取视频基础信息
    videoBaseUrl = 'https://admin.xiaoe-tech.com/xe.course.b_admin_r.resource.info/1.0.0?resource_id=' + resourceId
    headers = {
        'Cookie': cookie
    }
    videoBaseInfo = requests.get(videoBaseUrl, headers = headers).json()
    # print(videoBaseInfo)
    if videoBaseInfo['code'] != 0:
        print('获取视频基础信息失败')
        return

    title = videoBaseInfo['data']['title']
    imgUrl = videoBaseInfo['data']['img_url']

    # 2. 获取视频的视频文件信息
    videoFileUrl = 'https://admin.xiaoe-tech.com/xe.course.b_admin_r.video.info.get/1.0.0?resource_id=' + resourceId
    videoFileInfo = requests.get(videoFileUrl, headers = headers).json()
    # print(videoFileInfo)
    if videoFileInfo['code'] != 0:
        print('获取视频文件信息失败')
        return

    fileId = videoFileInfo['data']['file_id']
    fileName = videoFileInfo['data']['file_name']
    videoUrl = videoFileInfo['data']['video_url']
    videoLength = videoFileInfo['data']['video_length']
    videoSize = videoFileInfo['data']['video_size']

    # 3. 更新视频文件的所属课程和售卖设置，此处更新为属于指定的课程，且售卖设置改为不单独售卖
    payload = {
        "goods": {
            "status_info": {
                "is_display": True,
                "is_stop_sell": False,
                "is_timing_off": False,
                "is_timing_sale": False,
                "sale_at": "",
                "sale_status": 1,
                "timing_off": ""
            },
            "sell_data": {"is_single_sale": False}
        },
        "course": {
            "title": title,
            "img_url": imgUrl,
            "learn_page_cover": imgUrl,
            "descrb": ""
        },
        "content": {
            "file_id": fileId,
            "file_name": fileName,
            "video_url": videoUrl,
            "video_length": videoLength,
            "video_size": videoSize
        },
        "relation": {
            "add": [
                {
                    "resource_id": parentId,
                    "resource_type": parentType,
                    "sub_course_id": ""
                }
            ]
        },
        "resource_id": resourceId
    }
    updateVideoUrl = 'https://admin.xiaoe-tech.com/xe.course.b_admin_w.video.update/1.0.0'
    updateVideoResponse = requests.post(updateVideoUrl, headers = headers, json = payload)
    # print(updateVideoResponse.json())
    if updateVideoResponse.json()['code'] != 0:
        print('更新视频失败')
        return
    print('更新视频成功')

for resourceId in resourceIds:
    updateVideoParentAndSalesSettings(resourceId, parentId, parentType)