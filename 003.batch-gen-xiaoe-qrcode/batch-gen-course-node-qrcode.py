import requests
import qrcode

# 批量生成课程小节的二维码

# 需要先填充以下信息
cookie = """"""
courseId = ''

def genQrcode(content, fileName):
    for i,j in ("/／","\\＼","?？","|︱","\"＂","*＊","<＜",">＞"):
        fileName = fileName.replace(i,j)
    qrcode.make(content.strip()).save('%s.png' % fileName)

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

# 2. 依次生成各小节的二维码
headers = {
    'Cookie': cookie
}
for chapterDetail in chapterDetails:
    chapterId = chapterDetail['chapter_id']
    chapterTitle = chapterDetail['chapter_title']
    shareUrl = 'https://admin.xiaoe-tech.com/xe.course.b_admin_r.camp_pro.share.info.get/1.0.0'
    payload = {
        'course_id': courseId,
        'sub_course_id': '',
        'content_type': 3,
        'content_id': chapterId
    }
    response = requests.post(shareUrl, headers = headers, json = payload).json()
    if response['code'] != 0:
        print('获取章节二维码链接失败: ' + chapterTitle)
        continue
    qrcodeUrl = response['data']['short_content_url']
    genQrcode(qrcodeUrl, chapterTitle)
    print('%s, %s' % (qrcodeUrl, chapterTitle))

# 3. 生成课程合集二维码
shareUrl = 'https://admin.xiaoe-tech.com/xe.course.b_admin_r.share_url.get/1.0.0?resource_id=' + courseId
response = requests.get(shareUrl, headers = headers).json()
if response['code'] != 0:
    raise Exception('获取课程合集二维码链接失败')
qrcodeUrl = response['data']['h5']['short_url']
genQrcode(qrcodeUrl, '合集')
print('%s, %s' % (qrcodeUrl, '合集'))