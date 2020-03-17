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
                '<a href="javascript:void(0);" id="edit" onclick="_open_layer_info(\'' + Id + '\', \'content\');" ' +
                'title="编辑"><i class="icon-edit"></i></a> ' +
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

function ajax_submit_form($tag_name, $url, $data){
    var $tip_index;
    $($tag_name).ajaxSubmit({
            type: "post",
            dataType: "json",
            url: $url,
            data: $data,
            beforeSubmit: function () {
                $tip_index = open_handle_tip();
            },
            success: function (result) {
                var code = result.code;
                close_handle_tip($tip_index);
                if (code == 0) {
                    set_redirect_href(result.data);
                }
                else {
                    open_error_tip(result.msg);
                    return false;
                }
            },
            error: function (e) {
                if (e.status == 400) {
                    set_redirect_href("/login.html");
                }
                open_error_tip("系统繁忙,请稍后……");
                return false;
            }
        });
}

function removeMode($_id) {
    layer.confirm('你确定要删除该记录？删除后将不能恢复!', {
        btn: ['确定', '取消'],
        title: false
    }, function () {
        var $o = $("#" + $_id);
        var $data = $o.attr("data");
        var $url = $o.attr("other_data").split("|")[0];
        var $send_data = {"v": $data};
        return ajax_submit_form("form#dabai-button-content-form", $url, $send_data);
    });
}
function moveMode(Id, action) {
    $('#' + Id).unbind('click');
    var $is_pass = "";
    if (action == 'before') {
        if ($('#' + Id).prev('.editMode').length > 0) {
            $is_pass = "up";
        }
    } else {
        if ($('#' + Id).next('.editMode').length > 0) {
            $is_pass = "down";
        }
    }
    if ($is_pass != "") {
        layer.confirm('你确定要移动该记录？', {
             btn: ['确定', '取消'],
            title: false
        }, function () {
             var $o = $("#" + Id);
             var $data = $o.attr("data");
            var $url = $o.attr("other_data").split("|")[1];
            var $send_data = {"v": $data, "action": $is_pass};
            return ajax_submit_form("form#dabai-button-content-form", $url, $send_data);
        });
    }

}
