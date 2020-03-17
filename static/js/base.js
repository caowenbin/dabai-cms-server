function getCookie(name) {
    var $csrftoken = $('meta[name=csrf-token]').attr('content');
    return $csrftoken;
}
jQuery(function ($) {
    $('[data-toggle="tooltip"]').tooltip();
    var v = $("form[name='pop']").easyform();
    v.is_submit = false;
    $("#form_submit").on("click", function () {
        var tip_index;
        $(this).attr("disabled", true);
        $("form[name='pop']").ajaxSubmit({
            type: "post",
            dataType: "json",
            beforeSerialize: function () {
            },
            beforeSubmit: function () {
                var verify_result = verify_form_data();
                console.log("check", "verify_result:", verify_result, "is_submit:", v.is_submit);
                if (v.is_submit == false) {
                    $("#form_submit").attr("disabled", false);
                    return v.is_submit
                }

                if(verify_result == false){
                    $("#form_submit").attr("disabled", false);
                    return verify_result;
                }
                tip_index = open_handle_tip();
            },
            success: function (result) {
                var code = result.code;
                close_handle_tip(tip_index);
                if (code == 0) {
                    set_redirect_href(result.data);
                }
                else {
                    $("#form_submit").attr("disabled", false);
                    open_error_tip(result.msg);
                    return false;
                }
            },
            error: function (e) {
                if (e.status == 400) {
                    set_redirect_href("/login.html");
                }
                $("#form_submit").attr("disabled", false);
                open_error_tip("系统繁忙,请稍后……");
                return false;
            }
        });
    });
});
function set_redirect_href(_url) {
    window.location.href = _url;
}
function open_handle_tip() {
    var index = layer.msg('<i class="icon-spinner bigger-110"></i>正在操作……', {"time": 0});
    return index;
}

function open_error_tip(error_msg) {
    layer.msg(error_msg, {
        time: 5000, //20s后自动关闭
        btn: ['知道了'],
        icon: 2
    });
}
function close_handle_tip(index) {
    layer.close(index);
}
function _open_layer_info($url, $title, $width, $height) {
    if ($title == undefined) $title = '新增';
    if ($width == undefined) $width = '600px';
    if ($height == undefined) $height = '315px';

    layer.open({
        type: 2,
        title: $title,
        skin: 'layui-layer-rim', //加上边框
        area: [$width, $height], //宽高
        content: $url,
        cancel: function (index) {
            layer.closeAll('dialog');
        }
    });
}


function _operation_submit_form($url, $data){
    var $tip_index;
    $("form#dabai-button-content-form").ajaxSubmit({
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

function operation($url, $_id, $msg) {
    layer.confirm($msg, {
        btn: ['确定', '取消'],
        title: false
    }, function () {
        var $send_data = {"id": $_id};
        return _operation_submit_form($url, $send_data);
    });
}