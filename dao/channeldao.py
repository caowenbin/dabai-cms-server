#!/usr/bin/env python
# coding: utf8
import datetime

from extends import db
__author__ = 'ye shuo'


class ChannelDao(object):

    @staticmethod
    def save(channel_code, name, secret_key, remarks=None):
        """
        保存信息
        :param channel_code:
        :param name:
        :param secret_key:
        :param remarks:
        :return:
        """
        result = db.master.insert(
                tablename="channels",
                channel_code=channel_code,
                created_time=datetime.datetime.now(),
                name=name,
                secret_key=secret_key,
                remarks=remarks,
                validity=1
        )

        return result

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
        query_type = kwargs.get("query_type", -1)
        channel_code = kwargs.get("channel_code", "")
        name = kwargs.get("name", "")
        if query_type != -1:  # 有效的
            wheres.append(u"validity=$validity")
            values["validity"] = query_type

        if name:
            wheres.append(u"name like $name")
            values["name"] = u"%{}%".format(name)

        if channel_code:
            wheres.append(u"channel_code like $channel_code")
            values["channel_code"] = u"%{}%".format(channel_code)

        where_str = u" and ".join(wheres) if wheres else None

        return where_str, values

    @staticmethod
    def query_list(query_type=-1, channel_code=None, name=None, limit=None, offset=None, whats=None):
        """
        分页查询信息
        :param query_type: -1全部 1有效 0注销
        :param channel_code:
        :param name:
        :param limit:
        :param offset:
        :param whats:
        :return:
        """
        where_str, values = ChannelDao.__gen_wheres_values(
            query_type=query_type,
            channel_code=channel_code,
            name=name
        )

        if whats is None:
            whats = u"id,channel_code,name,remarks,secret_key,validity,updated_time"

        results = db.slave.select(
            tables=u'channels',
            what=whats,
            vars=values,
            where=where_str,
            limit=limit,
            offset=offset,
            order=u"updated_time DESC"
        )

        return results

    @staticmethod
    def get_total_count(query_type=-1, channel_code=None, name=None):
        """
        获取对应的条数
        :param query_type:
        :param channel_code:
        :param name:
        :return:
        """
        where_str, values = ChannelDao.__gen_wheres_values(
            query_type=query_type,
            channel_code=channel_code,
            name=name
        )

        counts = db.slave.select(
            tables='channels',
            what="count(id) as counts",
            vars=values,
            where=where_str
        ).first().counts

        return counts

    @staticmethod
    def get_detail(whats="*", _id=None, channel_code=None):
        """
        详情
        :param whats:
        :param _id:
        :param channel_code:
        :return:
        """
        where = {}
        if _id is not None:
            where["id"] = _id
        if channel_code is not None:
            where["channel_code"] = channel_code
        result = db.slave.select(tables=u"channels", what=whats, where=where).first()
        return result

    @staticmethod
    def update(_id, name=None, remarks=None, secret_key=None):
        """
        修改
        :param _id:
        :param name:
        :param remarks:
        :param secret_key:
        :return:
        """
        set_values = dict(name=name, secret_key=secret_key)

        if remarks is not None:
            set_values["remarks"] = remarks

        result = db.master.update('channels', vars={'id': _id}, where="id=$id ", **set_values)

        return result

    @staticmethod
    def delete(_ids):
        """
        批量删除
        :param _ids:
        :return:
        """
        result = db.master.delete('channels', vars={'ids': _ids}, where="id in $ids")

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

        result = db.master.update('channels', vars={'ids': ids}, where="id in $ids ", **set_values)

        return result

    @staticmethod
    def query_channel_by_code(channel_codes, whats="*"):
        """
        根据渠道编码列表查询对应的值
        :param channel_codes:
        :param whats:
        :return:
        """
        results = db.slave.select(
            tables=u'channels',
            what=whats,
            vars={"channel_codes": channel_codes},
            where=u"channel_code in $channel_codes"
        )

        return results

    @staticmethod
    def query_channel_tables():
        """
        查询渠道字典表
        :return:
        """
        channel_data = ChannelDao.query_list(whats=u"channel_code, name")
        channel_list = {c.channel_code: c.name for c in channel_data}
        return channel_list

channel = ChannelDao
