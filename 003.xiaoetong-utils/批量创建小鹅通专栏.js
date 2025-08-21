/**
 * 在大专栏下批量创建专栏，所创建的专栏不单独售卖、最新创建的排在最后、属于当前打开页面对应大专栏
 */

if (!window.location.href.match('https://admin.xiaoe-tech.com/t/course/big_column/detail/*')) {
    alert('请在大专栏详情页执行');
    throw new Error('不是在大专栏详情页创建专栏列表，中断执行');
}

// 需要创建的专栏名称
let columnTitles = [
    "字母 Aa /ə/",
];

// 倒序创建，这样在大专栏里顺序才是正的
columnTitles.reverse();

// 所属大专栏 ID
let tempArr = window.location.href.split('/');
let bigColumnId = tempArr[tempArr.length - 1];

let url = 'https://admin.xiaoe-tech.com/xe.course.b_admin_w.column.create/1.0.0';

console.log(bigColumnId);

for (columnTitle of columnTitles) {

    let payload = {
    "app": {"app_descrb": "", "app_img_url": ""},
    "content": {"relation_type": 1},
    "course": {
        "ct_flag": 0,
        "descrb": "",
        "img_url": "https://commonresource-1252524126.cdn.xiaoeknow.com/image/liyd8zub09di.png",
        "learn_page_cover": "https://commonresource-1252524126.cdn.xiaoeknow.com/image/liyd8zub09di.png",
        "learn_page_cover_mid": "",
        "org_content": "",
        "summary": "",
        "title": columnTitle
    },
    "goods": {
        "base_data": {
            "is_relative_sale": true,
            "is_single_sale": false,
            "resource_id": "",
            "resource_type": 6,
            "sku_id": "",
            "special": false,
            "spu_id": "",
            "spu_type": ""
        },
        "goods_group": {"customValue": []},
        "goods_list": [],
        "logistic_info": {"distribution_value": ["1"]},
        "sell_data": {"is_single_sale": false},
        "sku": [],
        "status_info": {
            "is_display": true,
            "is_stop_sell": false,
            "is_timing_off": false,
            "is_timing_sale": false,
            "sale_at": "",
            "sale_status": 1,
            "timing_off": ""
        }
    },
    "ios": {
        "descrb": "",
        "img_url": "",
        "org_descrb": "",
        "org_preview_content": "",
        "org_summary": null,
        "preview_content": "",
        "state": 0,
        "summary": null,
        "title": null,
        "video_slice_img_url": ""
    },
    "library_list": [],
    "relation": {
        "add": [
            {
                "resource_id": bigColumnId,
                "resource_type": 8,
                "sub_course_id": ""
            }
        ],
        "del": []
    },
    "scene": "1001"
};
    
    $.ajax({
        async: false,
        type: 'POST',
        url: url,
        data: JSON.stringify(payload),
        contentType: 'application/json',
        success: function(result, status) {
            if (!result || result.code !== 0) {
                alert('出错了，' + columnTitle);
            } else {
                console.log('专栏创建成功：' + columnTitle);
            }
        },
        error: function(xhr, status, error) {
            alert('出错了，' + columnTitle);
        }
    })
}