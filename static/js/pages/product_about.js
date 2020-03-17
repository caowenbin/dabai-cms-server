var wwei_editor = UE.getEditor('wwei_editor', {
    serverUrl: "/admin/ueditor/images/upload.html",
    toolbars: [[
        'autotypeset', '|',
        'bold', 'italic', 'underline',
        'fontsize', 'forecolor', 'backcolor', '|',
        'insertorderedlist',
        'lineheight', '|',
        'justifyleft', 'justifycenter', 'justifyright', 'justifyjustify', '|',
        'insertimage', '|', 'undo', 'redo', 'source'
    ]],
    autoHeightEnabled: false
});
wwei_editor.ready(function () {
    wwei_editor.addListener('contentChange', function () {
        $("#preview").html(wwei_editor.getContent());
    });
});

var wwei_editor_pad = UE.getEditor('wwei_editor_pad', {
    serverUrl: "/admin/ueditor/images/upload.html",
    textarea: "editorValue_pad",
    toolbars: [[
        'autotypeset', '|',
        'bold', 'italic', 'underline',
        'fontsize', 'forecolor', 'backcolor', '|',
        'insertorderedlist',
        'lineheight', '|',
        'justifyleft', 'justifycenter', 'justifyright', 'justifyjustify', '|',
        'insertimage', '|', 'undo', 'redo', 'source'
    ]],
    autoHeightEnabled: false
});
wwei_editor_pad.ready(function () {
    wwei_editor_pad.addListener('contentChange', function () {
        $("#preview").html(wwei_editor_pad.getContent());
    });
});

var child_data_tip;
function verify_form_data() {
    if (wwei_editor.getContent().length == 0 && wwei_editor_pad.getContent().length == 0) {
        child_data_tip.show();
        return false;
    }
    return true;
}


$(function () {
    /*模板Tab */
    child_data_tip = $('#templateContent').easytip();
    var dataType = 'imgtext';
    $("#content-pad").hide();

    function _loadtemp(dataType) {
        $("#template-loading").show();
        var tabPane = $("#temp-" + dataType);
        $.ajax({
            type: "POST",
            url: "/admin/product/about/template.html",
            data: {"type": dataType, "_xsrf": getCookie("_xsrf")},
            success: function (data) {
                $("#template-loading").hide();
                tabPane.html(data.data);
                var _tempLi = tabPane.find('.template-list li');
                _tempLi.hover(function () {
                    $(this).css({"background-color": "#f5f5f5"});
                }, function () {
                    $(this).css({"background-color": "#fff"});
                });
                _tempLi.click(function () {
                    var _tempHtml = $(this).html();
                    if ($("#content-phone").css("display") == "block") {
                        wwei_editor.execCommand('insertHtml', _tempHtml);
                        wwei_editor.undoManger.save();
                    }
                    if ($("#content-pad").css("display") == "block") {
                        wwei_editor_pad.execCommand('insertHtml', _tempHtml);
                        wwei_editor_pad.undoManger.save();
                    }
                });
            }
        });
    }

    _loadtemp(dataType);//加载
    //左边的TAB切换
    $('#templateTab a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
        dataType = $(this).attr("data-type");
        if (dataType) {
            var tabPane = $("#temp-" + dataType);
            if (tabPane.find('.template-list').length <= 0) {
                _loadtemp(dataType);
            }
        }
    });
    //Content切换
    $("#templateContent a").click(function (e) {
        e.preventDefault();
        $(this).tab('show');
        var dataType = $(this).attr("data-type");
        $("div#wxcontent>div[id*='content']").hide();
        $("#content-" + dataType).show();
    });
    //清空
    $('#clear-editor').click(function () {
        if ($("#content-phone").css("display") == "block") {
            wwei_editor.setContent("");
        }
        if ($("#content-pad").css("display") == "block") {
            wwei_editor_pad.setContent("");
        }
    });

    //预览效果
    $("#phoneclose").on('click', function () {
        $("#previewbox").hide()
    });
    $("#phone").on('click', function () {
        if ($("#content-phone").css("display") == "block") {
            $("#preview").html(wwei_editor.getContent());
        }
        if ($("#content-pad").css("display") == "block") {
            $("#preview").html(wwei_editor_pad.getContent());
        }
        if ($("#previewbox").css("display") == "block") {
            $("#previewbox").hide();
        } else {
            $("#previewbox").show();
        }
    });

});
