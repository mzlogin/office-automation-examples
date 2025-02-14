import requests

# 需要先填充 cookie、resourceIds、parentId、parentType 再运行

cookie = """"""

# resourceIds，过滤 https://admin.xiaoe-tech.com/xe.course.b_admin_r.course.base.list/1.0.0 请求所得
resourceIds = [
]

# 倒序，因为视频是按照倒序的顺序添加的
resourceIds.reverse()

parentId = ''
parentType = 50

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