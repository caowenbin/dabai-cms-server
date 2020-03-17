jQuery(function ($) {
    $('.nc-login-mode').tabulous({
        effect: 'flip'//动画反转效果
    });

    var div_form = '#default';
    $(".nc-login-mode .tabs-nav li a").click(function () {
        if ($(this).attr("href") !== div_form) {
            div_form = $(this).attr('href');
            $("" + div_form).find(".makecode").trigger("click");
        }
    });

    var ad_form = $("form[id='admin_form']").easyform();
    ad_form.is_submit = false;
    var sup_form = $("form[id='supplier_form']").easyform();
    sup_form.is_submit = false;
    $("#admin_submit").on("click", function () {
        var tip_index;
        $(this).attr("disabled", true);
        $("form[id='admin_form']").ajaxSubmit({
            type: "post",
            dataType: "json",
            beforeSerialize: function () {
            },
            beforeSubmit: function () {
                if (ad_form.is_submit == false) {
                    $("#admin_submit").attr("disabled", false);
                    return ad_form.is_submit
                }
                tip_index = layer.msg('<i class="icon-ok bigger-110"></i>正在登录……', {"time": 0});
            },
            success: function (result) {
                var code = result.code;
                layer.close(tip_index);
                if (code == 0) {
                    console.log("------", result.data)
                    window.location.href = result.data;
                }
                else {
                    $("#admin_submit").attr("disabled", false);
                    layer.msg(result.msg, {
                        time: 20000, //20s后自动关闭
                        btn: ['知道了'],
                        icon: 2
                    });
                    return false;
                }
            },
            error: function (e) {
                $("#admin_submit").attr("disabled", false);
                layer.msg("系统繁忙,请稍后……", {
                    time: 20000, //20s后自动关闭
                    btn: ['知道了'],
                    icon: 2
                });
                return false;
            }
        });
        return false;
    });
    $("#supplier_submit").on("click", function () {
        var tip_index;
        $(this).attr("disabled", true);
        $("form[id='supplier_form']").ajaxSubmit({
            type: "post",
            dataType: "json",
            beforeSerialize: function () {
            },
            beforeSubmit: function () {
                if (sup_form.is_submit == false) {
                    $("#supplier_submit").attr("disabled", false);
                    return sup_form.is_submit
                }
                tip_index = layer.msg('<i class="icon-ok bigger-110"></i>正在登录……', {"time": 0});
            },
            success: function (result) {
                var code = result.code;
                layer.close(tip_index);
                if (code == 0) {
                    window.location.href = result.data;
                }
                else {
                    $("#supplier_submit").attr("disabled", false);
                    layer.msg(result.msg, {
                        time: 20000, //20s后自动关闭
                        btn: ['知道了'],
                        icon: 2
                    });
                    return false;
                }
            },
            error: function (e) {
                $("#supplier_submit").attr("disabled", false);
                layer.msg("系统繁忙,请稍后……", {
                    time: 20000, //20s后自动关闭
                    btn: ['知道了'],
                    icon: 2
                });
                return false;
            }
        });
    });

});