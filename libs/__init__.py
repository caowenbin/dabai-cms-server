#!/usr/bin/env python
# coding: utf8

import os
from flask import current_app


def gen_image_temp_dir(dir_name):
    """
    生成图片临时目录
    :param dir_name:
    :return:
    """
    upload_medias_folder = current_app.config.get("UPLOAD_MEDIAS_FOLDER")
    if not upload_medias_folder:
        upload_medias_folder = os.getcwd() + u"/medias"
    temp_dir = upload_medias_folder + u"/{dir_name}/".format(dir_name=dir_name)
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    return temp_dir


def gen_log_dir(dir_path):
    """
    生成日志目录
    :param dir_path:
    :return:
    """
    if not dir_path:
        dir_path = os.curdir+'/logs'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path
