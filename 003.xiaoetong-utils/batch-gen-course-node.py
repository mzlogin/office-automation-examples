import requests

# 批量生成课程小节

# 需要先填充以下信息
cookie = """"""
if cookie is None or len(cookie) == 0 :
    raise Exception('Cookie 不能为空')

courseId = ''
if courseId is None or len(courseId) == 0:
    raise Exception('课程 ID 不能为空')

nodeNames = [ ]
if nodeNames is None or len(nodeNames) == 0:
    raise Exception('小节名称列表不能为空')

placeholderVideoId = ''
if placeholderVideoId is None or len(placeholderVideoId) == 0:
    raise Exception('占位视频 ID 不能为空')

# 1. 获取视频基础信息
videoBaseUrl = 'https://admin.xiaoe-tech.com/xe.course.b_admin_r.resource.info/1.0.0?resource_id=' + placeholderVideoId
headers = {
    'Cookie': cookie
}
videoBaseInfo = requests.get(videoBaseUrl, headers = headers).json()
# print(videoBaseInfo)
if videoBaseInfo['code'] != 0:
    raise Exception('获取视频基础信息失败')

title = videoBaseInfo['data']['title']
imgUrl = videoBaseInfo['data']['img_url']

# 2. 获取视频的视频文件信息
videoFileUrl = 'https://admin.xiaoe-tech.com/xe.course.b_admin_r.video.info.get/1.0.0?resource_id=' + placeholderVideoId
videoFileInfo = requests.get(videoFileUrl, headers = headers).json()
# print(videoFileInfo)
if videoFileInfo['code'] != 0:
    raise Exception('获取视频文件信息失败')

fileId = videoFileInfo['data']['file_id']
fileName = videoFileInfo['data']['file_name']
videoUrl = videoFileInfo['data']['video_url']
videoLength = videoFileInfo['data']['video_length']
videoSize = videoFileInfo['data']['video_size']

# 3. 依次使用占位视频信息生成小节
for nodeName in nodeNames:
    if nodeName is None or len(nodeName) == 0:
        raise Exception('小节名称不能为空')
    addNodeUrl = 'https://admin.xiaoe-tech.com/xe.course.b_admin_w.video.create/1.0.0'
    payload = {
        "auditGray": False,
        "content": {
            "ai_caption_open": 0,
            "can_select": 1,
            "cover_img_url": imgUrl,
            "entertaining_diversions_switch": 0,
            "file_id": fileId,
            "file_name": fileName,
            "h5_push_state": 0,
            "patch_img_url": imgUrl,
            "play_fast_state": 0,
            "play_multiple_state": 0,
            "transcoding_state": 0,
            "video_length": 5,
            "video_size": "0.01",
            "video_url": videoUrl
        },
        "course": {
            "cpro_ch_id": "0",
            "ct_flag": 0,
            "descrb": "",
            "img_url": "https://commonresource-1252524126.cdn.xiaoeknow.com/image/liye7aqe0yfc.png",
            "learn_page_cover": "https://commonresource-1252524126.cdn.xiaoeknow.com/image/liye7aqe0yfc.png",
            "learn_page_cover_mid": "",
            "org_content": "",
            "summary": "",
            "title": nodeName
        },
        "library_list": [],
        "relation": {
            "add": [
                {
                    "resource_id": courseId,
                    "resource_type": 50,
                    "sub_course_id": ""
                }
            ]
        }
    }
    headers = {
        'Cookie': cookie
    }
    response = requests.post(addNodeUrl, headers = headers, json = payload)
    if response.json()['code'] != 0:
        print('创建小节失败，名称：' + nodeName)
    print('创建小节成功，名称：' + nodeName)
