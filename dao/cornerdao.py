#!/usr/bin/env python
# coding: utf8
import datetime

from extends import db
__author__ = 'ye shuo'


class AdminCornerDao(object):
    """
    角标DAO
    """
    @staticmethod
    def __gen_wheres_values(**kwargs):
        """
        生成查询条件及值
        :param kwargs:
        :rtype tuple:
        :return:
        """
        wheres = []
        values = dict()
        group_name = kwargs.get("group_name", "")

        if group_name:
            wheres.append(u"group_name like $group_name")
            values["group_name"] = u"%{}%".format(group_name)

        where_str = u" and ".join(wheres) if wheres else None

        return where_str, values

    @staticmethod
    def query_list(whats=None, group_name=None, limit=None, offset=None):
        """
        分页查询信息
        :param whats: 返回的字段
        :param group_name:
        :param limit:
        :param offset:
        :return:
        """
        where_str, values = AdminCornerDao.__gen_wheres_values(group_name=group_name)

        if not whats:
            whats = u"id, group_name, created_time, image, updated_time"
        results = db.slave.select(
            tables=u"corner_marks",
            what=whats,
            vars=values,
            where=where_str,
            limit=limit,
            offset=offset,
            order=u"updated_time DESC"
        )

        return results

    @staticmethod
    def get_total_count(group_name=None):
        """
        获取对应的条数
        :param group_name:
        :return:
        """
        where_str, values = AdminCornerDao.__gen_wheres_values(group_name=group_name)

        counts = db.slave.select(
            tables=u'corner_marks',
            what=u"count(id) as counts",
            vars=values,
            where=where_str
        ).first().counts

        return counts

    @staticmethod
    def save(group_name, *images):
        created_time = datetime.datetime.now()
        insert_values = [{"group_name": group_name, "created_time": created_time, "image": img}
                         for img in images]

        _ids = db.master.multiple_insert(tablename="corner_marks", values=insert_values)

        return _ids

    @staticmethod
    def delete(_ids):
        """
        删除
        :param _ids:
        :return:
        """
        result = db.master.delete('corner_marks', vars={'ids': _ids}, where=u"id in $ids")

        return result

    @staticmethod
    def query_group_name_list():
        """
        所有的角标分组名
        :return:
        """

        results = db.slave.select(tables=u"corner_marks", what=u"group_name", group=u"group_name")

        return results

cornermark = AdminCornerDao

