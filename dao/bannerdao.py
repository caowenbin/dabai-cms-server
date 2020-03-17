# coding: utf-8

import datetime
from extends import db

__author__ = 'bin wen'


class BannerDao(object):
    @staticmethod
    def save(banner_code, name, banner_type, target, image_url, remark):
        """
        保存信息
        :param banner_code:
        :param name:
        :param banner_type:
        :param target:
        :param image_url:
        :param remark:
        :return:
        """
        result = db.master.insert(
            tablename="banners",
            banner_code=banner_code,
            name=name,
            created_time=datetime.datetime.now(),
            banner_type=banner_type,
            target=target,
            image=image_url,
            remark=remark
        )

        return result

    @staticmethod
    def update(_id, name, banner_type, target, image_url, remark):
        """
        修改
        :param _id:
        :param name:
        :param banner_type:
        :param target:
        :param image_url:
        :param remark:
        :return:
        """
        set_values = dict(name=name, banner_type=banner_type, target=target, image=image_url,
                          remark=remark)

        result = db.master.update('banners', vars={'id': _id}, where="id=$id ", **set_values)

        return result

    @staticmethod
    def delete(_ids):
        """
        批量删除
        :param _ids:
        :return:
        """
        result = db.master.delete('banners', vars={'ids': _ids}, where="id in $ids")

        return result

    @staticmethod
    def __gen_wheres_values(**kwargs):
        """
        生成查询条件及值
        :param kwargs:
        :rtype tuple:
        :return:
        """
        ids = kwargs.get("ids", [])
        name = kwargs.get("name", "")
        query_type = kwargs.get("query_type", -1)

        wheres = []
        values = dict()

        if ids:
            wheres.append(u"id in $ids")
            values["ids"] = ids

        if query_type != -1:  # 有效的
            wheres.append(u"validity=$validity")
            values["validity"] = query_type

        if name:
            wheres.append(u"name like $name")
            values["name"] = u"%{}%".format(name)

        where_str = u" and ".join(wheres) if wheres else None

        return where_str, values if values else None

    @staticmethod
    def query_list(query_type=-1, whats=None, name=None, limit=None, offset=None, ids=None):
        """
        分页查询信息
        :param query_type: -1全部 1有效 0注销
        :param whats: 返回的字段
        :param name:
        :param limit:
        :param offset:
        :param ids:
        :return:
        """
        where_str, values = BannerDao.__gen_wheres_values(name=name, query_type=query_type, ids=ids)
        if not whats:
            whats = (u"id, banner_type, banner_code, updated_time, name, target, image, remark, "
                     u"validity")
        results = db.slave.select(
            tables=u"banners",
            what=whats,
            vars=values,
            where=where_str,
            limit=limit,
            offset=offset,
            order=u"updated_time DESC"
        )

        return results

    @staticmethod
    def get_total_count(query_type=-1, name=None):
        """
        获取对应的条数
        :param query_type: -1全部 1有效 0注销
        :param name:
        :return:
        """
        where_str, values = BannerDao.__gen_wheres_values(name=name, query_type=query_type)
        counts = db.slave.select(
            tables=u"banners",
            what=u"count(id) as counts",
            vars=values,
            where=where_str
        ).first().counts

        return counts

    @staticmethod
    def get_detail(_id):
        """
        详情
        :param _id:
        :return:
        """
        result = db.slave.select(tables=u"banners", where={'id': _id}).first()
        return result

    @staticmethod
    def set_validity(ids, validity):
        """
        批量注销或激活
        :param ids:
        :param validity:
        :return:
        """
        set_values = dict(validity=validity)

        result = db.master.update('banners', vars={'ids': ids}, where="id in $ids ", **set_values)

        return result

banner = BannerDao
