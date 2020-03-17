// 实例化
var uploader = WebUploader.create({
    pick: {
        id: '#filePicker',
        label: '点击选择图片'
    },
    dnd: '#uploader .queueList',
    paste: document.body,

    accept: {
        title: 'Images',
        extensions: 'gif,jpg,jpeg,bmp,png',
        mimeTypes: 'image/*'
    },

    // swf文件路径
    swf: "",
    compress: false,
    auto: true,

    disableGlobalDnd: true,
    chunked: true,
    server: '',
    fileNumLimit: 5,
    fileSizeLimit: 5 * 1024 * 1024,    // 5 M
    fileSingleSizeLimit: 1 * 1024 * 1024    // 1 M
});

// 负责设封面
function setengFile(file) {
    $("div#uploader ul.filelist>li>p.title").each(function () {
        $(this).removeClass("li-feng");
    });
    $("div#uploader ul.filelist>li input[name='cover_page']").each(function () {
        $(this).attr('value', 1);
    });
    $('div#uploader ul.filelist>li#' + file.id + ' p.title').addClass("li-feng");
    $("li#" + file.id + " input[name='cover_page']").attr('value', 0);
}

//按名字设置封面图
function setengFilebyname(name) {
    $("div#uploader ul.filelist>li>p.title").each(function () {
        $(this).removeClass("li-feng");
    });
    $("div#uploader ul.filelist>li input[name='cover_page']").each(function () {
        $(this).attr('value', 1);
    });
    $('div#uploader ul.filelist>li[name=' + name + '] p.title').addClass("li-feng");
    $("li[name=" + name + "] input[name='cover_page']").attr('value', 0);
}

jQuery(function () {
    var $ = jQuery, $wrap = $('#uploader');
    $("div.queueList>ul.filelist>li").each(function () {
        var name = $(this).attr("name");
        var $btns = $("li[name=" + name + "]>div.file-panel");

        $(this).mouseenter(function () {
            $btns.stop().animate({height: 30});
        });
        $(this).mouseleave(function () {
            $btns.stop().animate({height: 0});
        });

        $btns.on('click', 'span', function () {
            var index = $(this).index(), deg;

            switch (index) {
                case 0:
                    setengFilebyname(name);
                    return;
                case 1:
                    var $li = $('li[name=' + name + ']');
                    $li.off().find('.file-panel').off().end().remove();
                    return;
            }

        });
    });

    // 图片容器
    var $queue = $("div.queueList>ul.filelist");
    if (!$queue.html()) {

        $queue = $('<ul class="filelist"></ul>')
            .appendTo($wrap.find('.queueList'));
    }
    // 状态栏，包括进度和控制按钮
    var $statusBar = $wrap.find('.statusBar'),

    // 文件总体选择信息。
        $info = $statusBar.find('.info'),

    // 上传按钮
        $upload = $('button.uploadBtn'),

    // 没选择文件之前的内容。
        $placeHolder = $wrap.find('.placeholder'),

    // 总体进度条
        $progress = $statusBar.find('.progress').hide(),

    // 添加的文件数量
        fileCount = $("div.queueList>ul.filelist li").length,

    // 添加的文件总大小
        fileSize = 0,

    // 优化retina, 在retina下这个值是2
        ratio = window.devicePixelRatio || 1,

    // 缩略图大小
        thumbnailWidth = 110 * ratio,
        thumbnailHeight = 110 * ratio,

    // 可能有pedding, ready, uploading, confirm, done.
        state = 'pedding',

    // 所有文件的进度信息，key为file id
        percentages = {},

        supportTransition = (function () {
            var s = document.createElement('p').style,
                r = 'transition' in s ||
                    'WebkitTransition' in s ||
                    'MozTransition' in s ||
                    'msTransition' in s ||
                    'OTransition' in s;
            s = null;
            return r;
        })();

    if (!WebUploader.Uploader.support()) {
        alert('Web Uploader 不支持您的浏览器！如果你使用的是IE浏览器，请尝试升级 flash 播放器');
        throw new Error('WebUploader does not support the browser you are using.');
    }


    function getCookie(name) {
        var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        return r ? r[1] : undefined;
    }

    uploader.on('uploadBeforeSend', function (obj, data, headers) {
        $.extend(headers, {
            "X-Xsrftoken": getCookie("_xsrf")
        });
    });
    uploader.on('uploadSuccess', function (file, response) {
        $("li#" + file.id + " input[name='picture_url'").attr('value', response.data);
        //console.log(file, response);
    });
    // 当有文件添加进来时执行，负责view的创建
    function addFile(file) {
        fileCount = $("div.queueList>ul.filelist li").length + 1;
        if (fileCount > uploader.options.fileNumLimit) {
            layer.msg("上传文件超过限制", {icon: 5});
            return
        }
        if (fileCount == 1) {
            var images_page = '<p class="title li-feng"></p>' +
                '<input type="checkbox" name="cover_page" style="display: none"  value="0" checked/>';
        }
        else {
            var images_page = '<p class="title"></p>' +
                '<input type="checkbox" name="cover_page" style="display: none"  value="1" checked/>';
        }
        var $li = $('<li id="' + file.id + '">' +
                images_page + '<input type="hidden" name="picture_id" id="picture_id" value="0">' +
                '<input  type="checkbox" name="picture_url" style="display: none"  value="" checked/>' +
                '<p class="imgWrap"></p>' +
                '<p class="progress"><span></span></p>' +
                '</li>'),

            $btns = $('<div class="file-panel">' +
                '<span class="feng margin-right-5">设封面</span>' +
                '<span class="cancel">删除</span>' +
                    //'<span class="rotateRight">向右旋转</span>' +
                    //'<span class="rotateLeft">向左旋转</span>' +
                '</div>').appendTo($li),
            $prgress = $li.find('p.progress span'),
            $wrap = $li.find('p.imgWrap'),
            $info = $('<p class="error"></p>'),

            showError = function (code) {
                switch (code) {
                    case 'exceed_size':
                        text = '文件大小超出';
                        break;

                    case 'interrupt':
                        text = '上传暂停';
                        break;

                    default:
                        text = '上传失败，请重试';
                        break;
                }

                $info.text(text).appendTo($li);
            };

        if (file.getStatus() === 'invalid') {
            showError(file.statusText);
        } else {
            // @todo lazyload
            $wrap.text('预览中');
            uploader.makeThumb(file, function (error, src) {
                if (error) {
                    $wrap.text('不能预览');
                    return;
                }

                var img = $('<img src="' + src + '">');
                $wrap.empty().append(img);
            }, thumbnailWidth, thumbnailHeight);

            percentages[file.id] = [file.size, 0];
            file.rotation = 0;
        }

        file.on('statuschange', function (cur, prev) {
            if (prev === 'progress') {
                $prgress.hide().width(0);
            } else if (prev === 'queued') {
                //$li.off( 'mouseenter mouseleave' );
                // $btns.remove();
            }
            //console.log(file, cur, prev);

            // 成功
            if (cur === 'error' || cur === 'invalid') {
                console.log(file.statusText);
                showError(file.statusText);
                percentages[file.id][1] = 1;
            } else if (cur === 'interrupt') {
                showError('interrupt');
            } else if (cur === 'queued') {
                percentages[file.id][1] = 0;
            } else if (cur === 'progress') {
                $info.remove();
                $prgress.css('display', 'block');
            } else if (cur === 'complete') {
                $li.append('<span class="success"></span>');
            }

            $li.removeClass('state-' + prev).addClass('state-' + cur);
        });

        $li.on('mouseenter', function () {
            $btns.stop().animate({height: 30});
        });

        $li.on('mouseleave', function () {
            $btns.stop().animate({height: 0});
        });

        $btns.on('click', 'span', function () {
            var index = $(this).index(),
                deg;

            switch (index) {
                case 0:
                    setengFile(file);
                    return;
                case 1:
                    uploader.removeFile(file);
                    return;

                case 2:
                    file.rotation += 90;
                    break;

                case 3:
                    file.rotation -= 90;
                    break;
            }

            if (supportTransition) {
                deg = 'rotate(' + file.rotation + 'deg)';
                $wrap.css({
                    '-webkit-transform': deg,
                    '-mos-transform': deg,
                    '-o-transform': deg,
                    'transform': deg
                });
            } else {
                $wrap.css('filter', 'progid:DXImageTransform.Microsoft.BasicImage(rotation=' + (~~((file.rotation / 90) % 4 + 4) % 4) + ')');
            }


        });

        $li.appendTo($queue);
    }

    // 负责view的销毁
    function removeFile(file) {
        var $li = $('#' + file.id);

        delete percentages[file.id];
        updateTotalProgress();
        $li.off().find('.file-panel').off().end().remove();
    }

    function updateTotalProgress() {
        var loaded = 0,
            total = 0,
            spans = $progress.children(),
            percent;

        $.each(percentages, function (k, v) {
            total += v[0];
            loaded += v[0] * v[1];
        });

        percent = total ? loaded / total : 0;

        spans.eq(0).text(Math.round(percent * 100) + '%');
        spans.eq(1).css('width', Math.round(percent * 100) + '%');
        updateStatus();
    }

    function updateStatus() {
        var text = '', stats;

        if (state === 'ready') {
            text = '选中' + fileCount + '张图片，共' +
                WebUploader.formatSize(fileSize) + '。';
        } else if (state === 'confirm') {
            stats = uploader.getStats();
            if (stats.uploadFailNum) {
                text = '已成功上传' + stats.successNum + '张照片，' +
                    stats.uploadFailNum + '张照片上传失败，<a class="retry" href="#">重新上传</a>失败图片或<a class="ignore" href="#">忽略</a>'
            }

        } else {
            stats = uploader.getStats();
            text = '共' + fileCount + '张（' +
                WebUploader.formatSize(fileSize) +
                '），已上传' + stats.successNum + '张';

            if (stats.uploadFailNum) {
                text += '，失败' + stats.uploadFailNum + '张';
            }
        }

        $info.html(text);
    }

    function setState(val) {
        var file, stats;

        if (val === state) {
            return;
        }

        $upload.removeClass('state-' + state);
        $upload.addClass('state-' + val);
        state = val;

        switch (state) {
            case 'pedding':
                $placeHolder.removeClass('element-invisible');
                $queue.parent().removeClass('filled');
                $queue.hide();
                $statusBar.addClass('element-invisible');
                uploader.refresh();
                break;

            case 'ready':
                $placeHolder.addClass('element-invisible');
                $('#filePicker2').removeClass('element-invisible');
                $queue.parent().addClass('filled');
                $queue.show();
                $statusBar.removeClass('element-invisible');
                uploader.refresh();
                break;

            case 'uploading':
                $('#filePicker2').addClass('element-invisible');
                $progress.show();
                $upload.text('暂停上传');
                break;

            case 'paused':
                $progress.show();
                $upload.text('继续上传');
                break;

            case 'confirm':
                $progress.hide();
                $upload.text('开始上传').addClass('disabled');

                stats = uploader.getStats();
                if (stats.successNum && !stats.uploadFailNum) {
                    setState('finish');
                    return;
                }
                break;
            case 'finish':
                stats = uploader.getStats();
                if (stats.successNum) {
                    // 上传成功的信息

                } else {
                    // 没有成功的图片，重设
                    state = 'done';
                    location.reload();
                }
                break;
        }

        updateStatus();
    }

    uploader.onUploadProgress = function (file, percentage) {
        var $li = $('#' + file.id),
            $percent = $li.find('.progress span');

        $percent.css('width', percentage * 100 + '%');
        percentages[file.id][1] = percentage;
        updateTotalProgress();
    };

    uploader.onFileQueued = function (file) {
        fileCount++;
        fileSize += file.size;

        if (fileCount === 1) {
            $placeHolder.addClass('element-invisible');
            $statusBar.show();
        }

        addFile(file);
        setState('ready');
        updateTotalProgress();
    };

    uploader.onFileDequeued = function (file) {
        fileCount--;
        fileSize -= file.size;

        if (!fileCount) {
            setState('pedding');
        }

        removeFile(file);
        updateTotalProgress();

    };

    uploader.on('all', function (type) {
        var stats;
        switch (type) {
            case 'uploadFinished':
                setState('confirm');
                break;

            case 'startUpload':
                setState('uploading');
                break;

            case 'stopUpload':
                setState('paused');
                break;

        }
    });

    uploader.onError = function (code) {
        var error_msg;
        if (code == "Q_EXCEED_NUM_LIMIT") {
            error_msg = "添加的图片数量超过限制,只能上传" + uploader.options.fileNumLimit + "张图片";
        }
        else if (code == "F_EXCEED_SIZE") {
            error_msg = "上传的图片过大,请保持在1M之下的图片";
        }
        else if (code == "F_DUPLICATE") {
            error_msg = "该图片已经存在";
        }
        else {
            error_msg = "未知错误:" + code;
        }
        layer.msg(error_msg, {icon: 5});
    };

    $upload.on('click', function () {
        if ($(this).hasClass('disabled')) {
            return false;
        }

        if (state === 'ready') {
            uploader.upload();
        } else if (state === 'paused') {
            uploader.upload();
        } else if (state === 'uploading') {
            uploader.stop();
        }
    });

    $info.on('click', '.retry', function () {
        uploader.retry();
    });

    $info.on('click', '.ignore', function () {
        $("div#uploader ul>li.state-error").each(function () {
            uploader.removeFile($(this).attr("id"));
            $(this).remove();
        });
    });

    $upload.addClass('state-' + state);
    updateTotalProgress();
});