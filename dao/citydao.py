#!/usr/bin/env python
# coding: utf8
from extends import db
__author__ = 'ye shuo'


class CityDao(object):

    @staticmethod
    def query_list(whats=None, limit=None, offset=None):
        """
        分页查询信息
        :param whats: 返回的字段
        :param limit:
        :param offset:
        :return:
        """
        if not whats:
            whats = (u"id, province_name, province_code, city_name, city_code, area_name, "
                     u"area_code, updated_time")
        results = db.slave.select(
            tables=u"cover_areas",
            what=whats,
            limit=limit,
            offset=offset
        )

        return results

    @staticmethod
    def save(*insert_values):
        with db.master.transaction():
            result = db.master.delete(table="cover_areas", where=u"1=1")
            if insert_values:
                result = db.master.multiple_insert(tablename="cover_areas", values=insert_values)

            return result


cities = CityDao
