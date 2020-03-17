function upload_custom_image() {
    layer.open({
        type: 2,
        title: "上传图片",
        skin: 'layui-layer-rim', //加上边框
        area: ['550px', '315px'], //宽高
        btn: ['确定', '取消'],
        yes: function (index) {
            var body = layer.getChildFrame('body', index);
            var $body = $(body.html());
            var img_list = new Array();
            $("input[name='picture_url']", $body).each(function (e) {
                img_list.push($(this).attr('value'));
            });
            if (img_list.length > 0) {
                $("#uploader_contents").html("");
                $.each(img_list, function (i) {
                    $('input[name="custom_image"]').attr('value', img_list[i]);
                    $("<img src='" + img_list[i] + "'>").appendTo("#uploader_contents");
                });
            }
            layer.close(index);
        },
        content: "/admin/images/upload.html?p=product&limit=1"
    });
}
function restart_corner_mark(t) {
    if (t == 1) {
        $("#update_corner_mark").hide();
        $("#corner_mark_select").css("display", "inline-block");
        $("#restart_corner_mark").css("display", "inline-block");
    }
    else {
        $("#corner_mark_select").hide();
        $("#restart_corner_mark").hide();
        $("#update_corner_mark").show();
        $("input[name='corner_mark_image']").removeAttr("checked");

    }
}
jQuery(function ($) {
    $(".chosen-select").chosen();
    $("select[name='corner_mark_group']").on("change", function () {
        $.ajax(
            {
                type: "get",
                url: "/admin/cornermark/group/list.html",
                data: {"group_name": $(this).val()},
                dataType: 'json',
                success: function (result) {
                    $("#corner_mark_image_list").html("");
                    var data = result.data;
                    $("#corner_mark_image_list").append('<label class="width-102"><input name="corner_mark_image" type="radio" class="ace" value="0"><span class="lbl">&nbsp;&nbsp;&nbsp;无</span></label>');

                    $.each(data, function (i) {
                        var o = data[i];
                        var img_path = o.image;
                        $(' <label><input name="corner_mark_image" type="radio" data="filter_easyform" class="ace" value="' +
                            img_path + '"><span class="lbl"><img src="' + img_path + '"></span></label>').appendTo("#corner_mark_image_list");
                    });

                }
            })
    });
    $("select[name='content_type']").on("change", function () {
        $("#content_code").html("");
        $("#content_code").chosen("destroy");
        $.ajax(
            {
                type: "get",
                url: "/select/content/list.html",
                data: {"content_type": $(this).val(), "req_page": "group_template"},
                dataType: 'json',
                success: function (result) {
                    var data = result.data;
                    $.each(data, function (i) {
                        $("<option value='" + data[i].id + "'>" + data[i].title + "</option>").appendTo("#content_code");
                    });

                    $(".chosen-select").chosen();
                }
            })
    });
})