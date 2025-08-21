import requests

# 批量更新小鹅通课程的章节标题

# 需要先填充以下信息
cookie = """"""
courseId = ''
replaceDicts = {
}

# 1. 获取课程章节列表
chapterDetailUrl = 'https://admin.xiaoe-tech.com/xe.course.b_admin_r.camp_pro.chapter.list.get/1.0.0'
chapterDetails = []
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
    chapterDetails += data['list']
    total = data['total']
    totalPage = total / 50 + 1
    if page >= totalPage:
        break
    page += 1
print('chapterDetails count: ' + str(len(chapterDetails)))

# 2. 更新课程章节标题
for chapterDetail in chapterDetails:
    chapterId = chapterDetail['chapter_id']
    originTitle = chapterDetail['chapter_title']
    title = originTitle
    for key, value in replaceDicts.items():
        title = title.replace(key, value)
    if title == originTitle:
        continue

    updateChapterUrl = 'https://admin.xiaoe-tech.com/xe.course.b_admin_w.fast.update.title/1.0.0'
    payload = {
        "resource_id": chapterId,
        "resource_title": title
    }
    headers = {
        'Cookie': cookie
    }
    response = requests.post(updateChapterUrl, headers = headers, json = payload).json()
    if response['code'] != 0:
        print('更新课程章节标题失败，原始：' + originTitle + '，更新后：' + title)
        print(response)
        break
    print('更新课程章节标题成功，原始：' + originTitle + '，更新后：' + title)