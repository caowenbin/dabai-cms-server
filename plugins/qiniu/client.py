#!/usr/bin/env python
# coding: utf8
__author__ = 'ye shuo'

import os
import logging
from requests import get

from qiniu import Auth, put_file, BucketManager

logger = logging.getLogger("API")


class QiNiuClient(object):
    def __init__(self):
        self.access_key = ""
        self.secret_key = ""
        self.bucket_name = ""
        self.auth = None
        self.bucket_manager = None
        self.qn_domain_name = ""

    def init_app(self, app):
        qiniu_config = app.config["QINIU"]
        self.access_key = qiniu_config["access_key"],
        self.secret_key = qiniu_config["secret_key"],
        self.bucket_name = qiniu_config["bucket_name"],
        self.qn_domain_name = qiniu_config["qn_domain_name"]

    def upload(self, qiniu_name=None, local_file=None):
        try:
            qn_url = ""
            if isinstance(qiniu_name, unicode):
                qiniu_name = qiniu_name.encode('utf8')
            token = self.auth_request.upload_token(self.bucket_name[0], qiniu_name, 3600)

            logger.info(u"请求七牛数据: {}--{}".format(qiniu_name, local_file))
            ret, info = put_file(token, qiniu_name, local_file)
            logger.info(u"七牛返回数据:　{}--{}".format(ret, info))

            if info.status_code == 200:
                key = ret.get("key", "")
                hash = ret.get("key", "")
                qn_url = u"{}{}".format(self.qn_domain_name, key)
            return qn_url
        except Exception as e:
            return e

    def delete_from_bucket(self, qiniu_name):
        try:
            ret, info = self.bucket_manager_request.delete(self.bucket_name[0],
                                                           qiniu_name.replace(self.qn_domain_name, ""))
            if info.status_code == 200 and not ret:
                return True
            else:
                return False
        except Exception as e:
            return e

    @property
    def auth_request(self):
        if not self.auth:
            self.auth = Auth(self.access_key[0], self.secret_key[0])
        return self.auth

    @property
    def bucket_manager_request(self):
        if not self.bucket_manager:
            self.bucket_manager = BucketManager(self.auth_request)
        return self.bucket_manager

    @staticmethod
    def get_keep_picture(keep_dir, picture_url):
        try:
            img_name = picture_url.split("/")[-1]
            img_dir = keep_dir.rstrip("/") + "/" + img_name
            if os.path.exists(img_dir):
                return True

            response = get(picture_url, stream=True)
            with open(img_dir, "w+") as f:
                f.write(response.content)
        except:
            return False
        else:
            return True