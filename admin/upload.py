# coding: utf-8
import json
import logging
import os
import re

from flask import request, current_app
from flask.ext.admin import expose
from werkzeug.utils import secure_filename

from extends import qn, csrf
from cores.adminweb import BaseHandler
from libs import gen_image_temp_dir
from libs.uploader import Uploader
from utils.helpers import utf8

__author__ = 'bin wen'

_log = logging.getLogger("ADMIN")


class UploadHandler(BaseHandler):
    ALLOWED_EXTENSIONS = ('txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif')

    def allowed_file(self, filename):
        """
        允许的文件类型的集合
        :param filename:
        :return:
        """
        return '.' in filename and filename.rsplit('.', 1)[1] in self.ALLOWED_EXTENSIONS

    @csrf.exempt
    @expose('/', methods=("POST", "GET"))
    @expose('/images/upload.html', methods=("POST", "GET"))
    def upload_images_view(self):
        """
        上传图片
        :return:
        """
        if request.method == "GET":
            img_dir = request.args.get("p", "product")
            limit = request.args.get("limit", 1)
            return self.render(template="upload.html", p=img_dir, limit=limit)
        else:
            upload_type = request.args.get("p")
            if upload_type == "product":
                dir_name = "product"
            elif upload_type == "cornermark":
                dir_name = "cornermark"
            elif upload_type == "banner":
                dir_name = "banner"
            else:
                dir_name = upload_type

            upload_temp_path = gen_image_temp_dir(dir_name)
            file_metas = request.files['file']
            filename = file_metas.filename
            if file and self.allowed_file(filename):
                filename = secure_filename(filename)
                file_path = os.path.join(upload_temp_path, filename)
                file_metas.save(file_path)
                qn_url = qn.upload(local_file=file_path)

                try:
                    os.remove(file_path)
                except Exception, e:
                    _log.exception(u"[UploadHandler] remove image temp file error. Error:{}".format(utf8(e.message)))

                return self.make_write(result_code=0, result_data=qn_url)

    def gen_config(self):
        # 解析JSON格式的配置文件
        static_path = current_app.config.get("STATIC_PATH")
        with open(os.path.join(static_path, 'webeditor', 'config.json')) as fp:
            try:
                # 删除 `/**/` 之间的注释
                config = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
            except:
                config = {}
        return config

    @csrf.exempt
    @expose('/ueditor/images/upload.html', methods=("GET", "POST"))
    def ueditor_upload(self):
        """
        百度UEditor富文本编辑器的媒体操作
        :return:
        """
        if request.method == "GET":
            return self.write(self.gen_config())

        else:
            action = request.args.get("action")
            upload_temp_path = gen_image_temp_dir("product_about")
            config_list = self.gen_config()
            result = {}
            if action in ('uploadimage', 'uploadvideo'):
                # 图片、文件、视频上传
                if action == 'uploadimage':
                    field_name = config_list.get('imageFieldName')
                    config = {
                        "pathFormat": config_list['imagePathFormat'],
                        "maxSize": config_list['imageMaxSize'],
                        "allowFiles": config_list['imageAllowFiles']
                    }
                elif action == 'uploadvideo':
                    field_name = config_list.get('videoFieldName')
                    config = {
                        "pathFormat": config_list['videoPathFormat'],
                        "maxSize": config_list['videoMaxSize'],
                        "allowFiles": config_list['videoAllowFiles']
                    }
                if field_name in request.files:
                    field = request.files[field_name]
                    uploader = Uploader(field, config, upload_temp_path)
                    result = uploader.getFileInfo()
                    file_path = result["url"]
                    qn_url = qn.upload(local_file=file_path)
                    if isinstance(qn_url, Exception) or not qn_url:
                        result['state'] = '上传接口出错'
                    result["url"] = qn_url
                    try:
                        os.remove(file_path)
                    except Exception, e:
                        _log.exception(u"[UEditorUploadHandler] remove image temp file error.")
                else:
                    result['state'] = '上传接口出错'
            return self.write(result)
