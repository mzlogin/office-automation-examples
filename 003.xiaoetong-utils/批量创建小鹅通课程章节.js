/**
 * 在课程里批量创建章节
 */
if (!window.location.href.match('https://admin.xiaoe-tech.com/t/course/camp_pro/detail/*')) {
    alert('请在课程详情页执行');
    throw new Error('不是在课程详情页创建章节列表，中断执行');
}

let chapterTitles = [
    "章节名称数组",
];
let url = 'https://admin.xiaoe-tech.com/xe.course.b_admin_w.camp_pro.chapter.create/1.0.0';

let tempArr = window.location.href.split('/');
let courseId = tempArr[tempArr.length - 1];

console.log(courseId);

for (chapterTitle of chapterTitles) {

    let payload = {
        "course_id":courseId,
        "chapter_title":chapterTitle,
        "describe":chapterTitle,
        "sub_course_id":"",
        "chapter_state":0
    };
    
    $.ajax({
        async: false,
        type: 'POST',
        url: url,
        data: JSON.stringify(payload),
        contentType: 'application/json',
        success: function(result, status) {
            if (!result || result.code !== 0) {
                alert('出错了，' + chapterTitle);
            } else {
                console.log('章节创建成功：' + chapterTitle);
            }
        },
        error: function(xhr, status, error) {
            alert('出错了，' + chapterTitle);
        }
    })
}