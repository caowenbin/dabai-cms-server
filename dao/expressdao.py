#!/usr/bin/env python
# coding: utf8
import datetime

from extends import db
from configs.constants.refund import RefundStatus
from dao.orderdao import orders
from configs.constants.order import OrderStatus
from dao.refunddao import refund

__author__ = 'ye shuo'


class ExpressDao(object):
    @staticmethod
    def query_express(track_number=None, order_no=None):
        """

        :param track_number: 运单号
        :param order_no: 订单号
        :return:
        """
        if not track_number and not order_no:
            return []
        wheres = []
        values = {}
        if track_number:
            wheres.append(u"track_number=$track_number")
            values["track_number"] = track_number

        if order_no:
            wheres.append(u"record_value=$record_value")
            values["record_value"] = order_no

        result = db.slave.select(
                tables=u"express",
                what=u"id, updated_time, track_number, record_value",
                vars=values,
                where=u" and ".join(wheres) if wheres else None,
                order=u"created_time DESC"
        ).first()

        return result

    @staticmethod
    def express_update_by_id(**kwargs):
        _id = kwargs.pop("_id")
        result = db.master.update('express', vars={'id': _id}, where="id=$id ", **kwargs)
        return result

    @staticmethod
    def show_express_detail(record_type, record_value):
        """
        查看对应的快递单号
        :param record_type:
        :param record_value:
        :return:
        """
        result = db.slave.select(
                tables=u"express",
                what=u"*",
                where={"record_type": record_type, "record_value": record_value}
        ).first()
        return result

    @staticmethod
    def save(record_type, record_value, track_no, express_code):
        """
        保存快递单号信息
        :param record_type: 记录类型 0 订单发货单 1 退款发货单
        :param record_value:记录值 对应的各单的单号
        :param track_no: 快递单号
        :param express_code: 快递公司代号
        :return:
        """
        with db.master.transaction():
            express_id = db.master.insert(
                tablename="express",
                created_time=datetime.datetime.now(),
                record_type=record_type,
                record_value=record_value,
                track_number=track_no,
                express_code=express_code,
                status=0
            )

            if record_type == 0:
                orders.update(order_no=record_value, status=OrderStatus.Shipped.value)
            elif record_type == 1:
                refund.update(refund_no=record_value,
                              status=RefundStatus.BuyerReturnWaitSellerConfirm.value
                              )

            return express_id

express = ExpressDao
