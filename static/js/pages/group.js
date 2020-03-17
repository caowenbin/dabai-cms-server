function allMenu() {
    for (var i = 0; i < $('.editMode').length; i++) {
        showMenu($('.editMode').eq(i).attr('id'));
    }
}
function showMenu(Id) {
    $('#' + Id).hover(function () {
        if ($('#editorMenu').length < 1) {
            $('#' + Id).prepend('<div id="editorMenu">' +
                '<div id="editorMenubox">' +
                '<a href="javascript:void(0);" id="remove" onclick="removeMode(\'' + Id + '\');" ' +
                'title="删除"><i class="icon-trash"></i></a>' +
                ' <a href="javascript:void(0);" id="up" onmousedown="moveMode(\'' + Id + '\',\'before\')" ' +
                'title="上移"><i class="icon-arrow-up"></i></a> ' +
                '<a href="javascript:void(0);" id="down" onmousedown="moveMode(\'' + Id + '\',\'after\')" ' +
                'title="下移"><i class="icon-arrow-down"></i></a>' +
                '<br class="clear" /></div></div>');
        }
    }, function () {
        $('#editorMenu').remove();
    });
}
function removeMode($Id) {
    var $remove_template_index = layer.confirm('你确定要删除该模板？删除后此模板绑定的数据将删除并不能恢复!', {
        btn: ['确定', '取消'],
        title: false
    }, function () {
         $('#' + $Id).remove();
        layer.close($remove_template_index);
    });
}
function moveMode(Id, action) {
    $('#' + Id).unbind('click');
    if (action == 'before') {
        if ($('#' + Id).prev('.editMode').length > 0) {
            $('#' + Id).slideUp(300, function () {
                $('#' + Id).prev('.editMode').before($('#' + Id));
                $('#' + Id).slideDown(300);
            });
        }
    } else {
        if ($('#' + Id).next('.editMode').length > 0) {
            $('#' + Id).slideUp(300, function () {
                $('#' + Id).next('.editMode').after($('#' + Id));
                $('#' + Id).slideDown(300);
            });
        }
    }
}
function upload_icon(o) {
    layer.open({
        type: 2,
        title: "上传图片",
        skin: 'layui-layer-rim', //加上边框
        area: ['550px', '415px'], //宽高
        btn: ['确定', '取消'],
        yes: function (index) {
            var body = layer.getChildFrame('body', index);
            var $body = $(body.html());
            var img_list = new Array();
            $("input[name='picture_url']", $body).each(function (e) {
                img_list.push($(this).attr('value'));
            });
            if (img_list.length > 0) {
                var _data = $(o).attr("data");
                $("#uploader_contents-" + _data).html("");
                $.each(img_list, function (i) {
                    $('input[name="icon_url"]', $($(o).parents(".list-unstyled"))).each(function (e) {
                        $(this).attr('value', img_list[i]);
                    });
                    $("<img src='" + img_list[i] + "'>").appendTo("#uploader_contents-" + _data);
                });
            }
            layer.close(index);
        },
        content: "/admin/images/upload.html?p=group_icon&limit=1"
    });
}
function show_upload_button(o) {

    var _data = $(o).attr("data");
    if (o.checked) {
        $("#uploader_desc-" + _data).hide();
        $("#uploader_button-" + _data).show();
        $('input[name="is_show_icon"]', $($(o).parents(".list-unstyled"))).each(function (e) {
            $(this).attr('value', 1);
        });
    }
    else {
        $("#uploader_desc-" + _data).show();
        $("#uploader_button-" + _data).hide();
        $('input[name="is_show_icon"]', $($(o).parents(".list-unstyled"))).each(function (e) {
            $(this).attr('value', 0);
        });
    }
}

function set_show_name(o) {
    if (o.checked) {
        $('input[name="is_show_name"]', $($(o).parents(".list-unstyled"))).each(function (e) {
            $(this).attr('value', 1);
        });
    }
    else {
        $('input[name="is_show_name"]', $($(o).parents(".list-unstyled"))).each(function (e) {
            $(this).attr('value', 0);
        });
    }
}

function show_group_templates(url) {
    layer.open({
        type: 2,
        title: "选择模板",
        skin: 'layui-layer-rim', //加上边框
        area: ['500px', '415px'], //宽高
        content: url
    });
}

var $child_data_tip;
function verify_form_data() {
    var $template_o = $('div.group-templates>div.editMode');
    var $size = $template_o.length;
    if ($size == 0) {
        $child_data_tip.show();
        return false;
    }
    var $is_not_pass = false;
    var $is_not_index = 0;
    $template_o.each(function (index, domEle) {
        var $data = $(this).attr("data");
        if($data == "T-006" && $size-1 != index){
            $is_not_pass = true;
            $is_not_index = index+1;
            return
        }
    });
    if($is_not_pass){
        $child_data_tip.show("模板6(瀑布流模板)的位置必为最后一个模板,此次的模板6的位置设为第"+$is_not_index+"位置");
        return false;
    }
    return true;
}

$(document).ready(function (e) {
    $(".chosen-select").chosen();
    allMenu();
    $child_data_tip = $('#select-group-templates').easytip();
});