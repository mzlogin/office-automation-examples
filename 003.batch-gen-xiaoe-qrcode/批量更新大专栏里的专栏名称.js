// 页码数量，自行填充
let pageCount = ${};
// 店铺 appId，自行填充
let appId = ${};
// 标题里的原始字符串与新字符串
let oldStr = ${};
let newStr = ${};

if (!window.location.href.match('https://admin.xiaoe-tech.com/t/course/big_column/detail/*')) {
    alert('请在大专栏详情页执行');
    throw new Error('不是在大专栏详情页更专栏名称，中断执行');
}

function columnTitleReplace(columnToChange, oldStr, newStr) {
    let columnTitleUpdateUrl = 'https://admin.xiaoe-tech.com/xe.course.b_admin_w.fast.update.title/1.0.0';
    let resourceId = columnToChange.resource_id;
    let resourceName = columnToChange.resource_name.replace(oldStr, newStr);

    if (resourceName === columnToChange.resource_name) {
        console.log('不用处理，忽略，标题：' + columnToChange.resource_name);
        return;
    }
    
    let columnTitleUpdateData = {
        resource_id: resourceId,
        resource_title: resourceName
    };
    $.ajax({
        async: false,
        url: columnTitleUpdateUrl,
        data: columnTitleUpdateData,
        type: "POST",
        headers: {
            'Content-type': 'application/x-www-form-urlencoded'
        },
        success: function(result, status) {
            if (!result || result.code !== 0) {
                alert('出错了，标题：' + columnToChange.resource_name);
            }
            console.log('处理成功，标题：' + columnToChange.resource_name)
        },
        error: function(xhr, status, error) {
            alert('出错了，标题：' + columnToChange.resource_name);
        }
    });
}

let tempArr = window.location.href.split('/');
let bigColumnId = tempArr[tempArr.length - 1];

let columnListUrl = 'https://admin.xiaoe-tech.com/xe.course.b_admin_r.column.list/1.0.0';
// 循环获取每页的专栏，然后依次更新页内的每个标题
for (let i = 1; i <= pageCount; i++) {
    let queryColumnListData = {
        app_id: appId,
        resource_id: bigColumnId,
        state: -1,
        page: i,
        page_size: 50,
        resource_types: 6
    };
    $.ajax({
        async: false,
        url: columnListUrl,
        data: queryColumnListData,
        type: "POST",
        headers: {
            'Content-type': 'application/x-www-form-urlencoded'
        },
        success: function(result, status) {
            if (!result || result.code !== 0) {
                alert('出错了，页码' + i);
            } else {
                for (let j = 0; j < result.data.list.length; j++) {
                    let columnToChange = result.data.list[j];
                    columnTitleReplace(columnToChange, oldStr, newStr);
                }
            }
        },
        error: function(xhr, status, error) {
            alert('出错了，页码' + i);
        }
    });
}