#!/usr/bin/env python
# coding: utf8
import datetime

from extends import db

__author__ = 'ye shuo'


class SyncCMSDao(object):

    @staticmethod
    def query_list(whats="*"):
        results = db.slave.select(tables=u"cms_content", what=whats)
        return results

    @staticmethod
    def get_detail(_id, whats="*"):
        """
        模板内容详情
        :param whats:
        :param _id:
        :return:
        """
        result = db.slave.select(tables=u"cms_content", where={"id": _id}).first()
        return result

    @staticmethod
    def __gen_template_content_values(**kwargs):
        """
        解析生成模板内容值
        :param kwargs:
        :return:
        """
        set_values = {}

        if "content_type" in kwargs:
            set_values["type"] = kwargs["content_type"]

        if "content_code" in kwargs:
            set_values["target"] = kwargs["content_code"]

        if "custom_image" in kwargs:
            set_values["image"] = kwargs["custom_image"]

        if "custom_image_size" in kwargs:
            set_values["custom_image_size"] = kwargs["custom_image_size"]

        if "ordering" in kwargs:
            set_values["ordering"] = kwargs["ordering"]

        return set_values

    @staticmethod
    def save_template_content(**kwargs):
        """
        保存模板内容信息
        :param kwargs:
        :return:
        """
        insert_values = SyncCMSDao.__gen_template_content_values(**kwargs)
        insert_values["created_time"] = datetime.datetime.now()
        result = db.master.insert(tablename="cms_content", **insert_values)

        return result

    @staticmethod
    def update_template_content(_id, **kwargs):
        """
        修改模板内容信息
        :param _id:
        :param kwargs:
        :return:
        """
        set_values = SyncCMSDao.__gen_template_content_values(**kwargs)
        result = db.master.update(tables='cms_content', where={'id': _id}, **set_values)

        return result

    @staticmethod
    def delete_template_content(_id):
        """
        删除模板内容
        :param _id:
        :return:
        """
        result = db.master.delete('cms_content', where={"id": _id})

        return result


kit_cms = SyncCMSDao
