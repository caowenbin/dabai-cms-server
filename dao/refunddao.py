#!/usr/bin/env python
# coding: utf8
import datetime

from extends import db
from dao.orderdao import orders

__author__ = 'ye shuo'


class RefundDao(object):

    @staticmethod
    def save(picture_urls=None, **values):
        """
        保存信息
         :param picture_urls:
        :param values:
        :return:
        """
        if "created_time" not in values:
            values["created_time"] = datetime.datetime.now()
        with db.master.transaction():
            _id = db.master.insert(tablename="refunds", **values)
            if picture_urls:
                evidence_ids = RefundDao.save_refund_image(_id, picture_urls)

            # 设订单为取消状态
            set_order_cancel = orders.update(_id=values["order_id"], status=5)
            return _id

    @staticmethod
    def save_refund_image(refund_id, image_urls):
        """
        保存退款凭证
        :param refund_id:
        :param image_urls:
        :return:
        """
        now_time = datetime.datetime.now()
        insert_values = [{"refund_id": refund_id,
                          "evidence_image": img_url,
                          "created_time": now_time
                          } for img_url in image_urls]
        _ids = db.master.multiple_insert("refund_evidences", insert_values)
        return _ids

    @staticmethod
    def __parse_update_data(**kwargs):
        """
        解析修改退款信息
        :param kwargs:
        :return:
        """
        set_value = {}
        if "status" in kwargs:
            set_value["refund_status"] = kwargs["status"]

        return set_value

    @staticmethod
    def update(_id=None, refund_no=None, wheres=None, picture_urls=None, **kwargs):
        """
        修改退款信息
        :param _id:
        :param refund_no:
        :param wheres:
        :param picture_urls:
        :param kwargs:
        :return:
        """
        _values = RefundDao.__parse_update_data(**kwargs)
        where = {}
        if _id is not None:
            where["id"] = _id

        if refund_no is not None:
            where["refund_no"] = refund_no

        if wheres:
            where.update(wheres)
        with db.master.transaction():
            result = db.master.update(tables='refunds', where=where, **_values)
            if picture_urls:
                evidence_ids = RefundDao.save_refund_image(_id, picture_urls)
            return result

    @staticmethod
    def __gen_wheres_values(is_show_supplier=False, **kwargs):
        """
        生成查询条件及值
        :param kwargs:
        :rtype tuple:
        :return:
        """
        order_no = kwargs.get("order_no", "")
        start_time = kwargs.get("start_time", "")
        end_time = kwargs.get("end_time", "")
        supplier_id = kwargs.get("supplier_id", "")
        refund_status = kwargs.get("refund_status", "")
        query_type = int(kwargs.get("query_type", -1))

        wheres = [u"supplier_id = sp.id"] if is_show_supplier else []
        values = dict()

        if query_type != -1:
            wheres.append(u"refund_status=$refund_status")
            values["refund_status"] = query_type

        if order_no:
            wheres.append(u"order_no like $order_no")
            values["order_no"] = u"%{}%".format(order_no)

        if start_time:
            wheres.append(u"r.created_time >= $start_time")
            values["start_time"] = start_time

        if end_time:
            wheres.append(u"r.created_time <= $end_time")
            values["end_time"] = end_time

        if supplier_id:
            wheres.append(u"supplier_id=$supplier_id")
            values["supplier_id"] = u"{}".format(supplier_id)

        if refund_status or isinstance(refund_status, int):
            wheres.append(u"refund_status=$refund_status")
            values["refund_status"] = u"{}".format(refund_status)

        where_str = u" and ".join(wheres) if wheres else None

        return where_str, values if values else {}

    @staticmethod
    def query_list(whats=None, is_show_supplier=True, limit=None, offset=None, **kwargs):
        """
        分页查询信息 query_type -1代表全部,其他值都是对应的订单状态
        :param whats:
        :param is_show_supplier:
        :param limit:
        :param offset:
        :param kwargs:
        :return:
        """

        where_str, values = RefundDao.__gen_wheres_values(is_show_supplier, **kwargs)
        tables = u'refunds as r'
        if not whats:
            whats = u"r.*"

            if is_show_supplier:
                whats += u",sp.fullname as supplier_name"
                tables = [u'refunds as r', u"suppliers as sp"]

        results = db.slave.select(
            tables=tables,
            what=whats,
            vars=values,
            where=where_str,
            limit=limit,
            offset=offset,
            order=u"r.created_time DESC"
        )

        return results

    @staticmethod
    def get_total_count(**kwargs):
        """
        获取对应的条数
        :param kwargs:
        :return:
        """
        where_str, values = RefundDao.__gen_wheres_values(**kwargs)
        counts = db.slave.select(
            tables='refunds as r',
            what="count(id) as counts",
            vars=values,
            where=where_str
        ).first().counts

        return counts

    @staticmethod
    def get_detail(_id, whats=u"*"):
        """
        查看详情
        :param _id:
        :param whats:
        :return:
        """
        result = db.slave.select(tables="refunds", what=whats, where={"id": _id}).first()
        return result

    @staticmethod
    def query_refund_evidences(refund_id):
        """
        查询退款凭证图
        :param refund_id:
        :return:
        """

        results = db.slave.select(
                tables=u"refund_evidences",
                what="evidence_image, created_time",
                where={'refund_id': refund_id},
                order=u"created_time DESC"
        )
        return results


refund = RefundDao
