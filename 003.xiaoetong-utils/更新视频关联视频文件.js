const sleep = (delay) => new Promise((resolve) => setTimeout(resolve, delay));

async function asyncForEach(array, callback) {
    for (let index = 0; index < array.length; index++) {
        await callback(array[index], index, array);
    }
}

/**
 * 将视频关联的文件更新为与视频标题一致的视频文件
 */
if (!window.location.href.match('https://admin.xiaoe-tech.com/t/course/video/detail/*')) {
    alert('请在视频详情页执行');
    throw new Error('不是在视频详情页更新视频文件，中断执行');
}

async function updateVideoRelateFile() {
    // 获取视频标题
    var videoTitle = document.querySelector('.course-title').textContent.trim();

    // 点击选择文件按钮
    document.querySelector('.video-selector__right .ss-button').click()

    // 等待选择视频框出现
    do {
        await sleep(100);
        var videoSelectDialog = document.querySelector('.ss-material');
        if (videoSelectDialog && videoSelectDialog.style && videoSelectDialog.style.display != 'none') {
            var videoList = document.querySelectorAll('.z-table-selection');
            if (videoList && videoList.length === 10) {
                break;
            }
        }
    } while (true);

    await sleep(500);

    // 填充视频文件名
    var keywordInput = document.querySelector('.ss-material-main-right .ss-material-search__input');
    keywordInput.value = videoTitle;
    var event = document.createEvent('Event');
    event.initEvent("input", true, true);
    event.eventType = 'message'
    keywordInput.dispatchEvent(event)

    await sleep(100);

    // 点击搜索
    document.querySelector('.ss-material-main-right .ss-material-search__icon').click();

    // 判断如果只有唯一选项，则勾选并点击确定
    var i = 0;
    var found = false;
    do {
        await sleep(500);

        var videoList = document.querySelectorAll('.z-table-selection');
        if (videoList && videoList.length >= 1) {
            if (videoList.length === 10) {
                // 说明数据还没刷新
                continue;
            }
            if (videoList.length === 1) {
                videoList[0].click();
                found = true;
                await sleep(50);
            }
            break;
        }
    } while (i++ != 10);

    if (!found) {
        alert('没有找到唯一匹配视频，请手动处理');
    } else {
        document.querySelector('.ss-material-box-bottom .ss-button__primary').click();

        await sleep(500);

        // 点保存
        document.querySelector('.save-area__real .ss-button').click();
    }
}

await updateVideoRelateFile();