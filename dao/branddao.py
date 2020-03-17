#!/usr/bin/env python
# coding: utf8
import datetime

from extends import db

__author__ = 'ye shuo'


class AdminBrandDao(object):
    @staticmethod
    def save(name):
        """
        保存信息
        :param name:
        :return:
        """
        result = db.master.insert(tablename="brands", name=name, created_time=datetime.datetime.now())

        return result

    @staticmethod
    def update(_id, name):
        """
        修改
        :param _id:
        :param name:
        :return:
        """
        set_values = dict(name=name)

        result = db.master.update('brands', vars={'id': _id}, where="id=$id ", **set_values)

        return result

    @staticmethod
    def delete(_ids):
        """
        批量删除
        :param _ids:
        :return:
        """
        result = db.master.delete('brands', vars={'ids': _ids}, where="id in $ids")

        return result

    @staticmethod
    def __gen_wheres_values(**kwargs):
        """
        生成查询条件及值
        :param kwargs:
        :rtype tuple:
        :return:
        """
        name = kwargs.get("name", "")

        wheres = []
        values = dict()

        if name:
            wheres.append(u"name like $name")
            values["name"] = u"%{}%".format(name)

        where_str = u" and ".join(wheres) if wheres else None

        return where_str, values if values else None

    @staticmethod
    def query_list(whats=None, name=None, limit=None, offset=None):
        """
        分页查询信息
        :param whats: 返回的字段
        :param name:
        :param limit:
        :param offset:
        :return:
        """
        where_str, values = AdminBrandDao.__gen_wheres_values(name=name)
        if not whats:
            whats = u"id, created_time, updated_time, name"
        results = db.slave.select(
            tables=u"brands",
            what=whats,
            vars=values,
            where=where_str,
            limit=limit,
            offset=offset,
            order=u"updated_time DESC"
        )

        return results

    @staticmethod
    def get_total_count(name=None):
        """
        获取对应的条数
        :param name:
        :return:
        """
        where_str, values = AdminBrandDao.__gen_wheres_values(name=name)
        counts = db.slave.select(
            tables=u"brands",
            what=u"count(id) as counts",
            vars=values,
            where=where_str
        ).first().counts

        return counts


brands = AdminBrandDao
