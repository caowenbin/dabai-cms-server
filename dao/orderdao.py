#!/usr/bin/env python
# coding: utf8
from extends import db
from configs.constants.order import OrderStatus
__author__ = 'ye shuo'


class AdminOrderDao(object):
    @staticmethod
    def __gen_wheres_values(is_show_supplier=False, **kwargs):
        """
        生成查询条件及值
        :param kwargs:
        :rtype tuple:
        :return:
        """
        query_type = int(kwargs.get("query_type", -1))
        order_no = kwargs.get("order_no")
        receiver_phone = kwargs.get("receiver_phone")
        start_time = kwargs.get("start_time")
        end_time = kwargs.get("end_time")
        trade_no = kwargs.get("trade_no")
        channel_code = kwargs.get("channel_code")
        supplier_id = kwargs.get("supplier_id")

        wheres = [u"supplier_id = sp.id"] if is_show_supplier else []
        values = dict()

        if query_type != -1:
            wheres.append(u"order_status=$order_status")
            values["order_status"] = query_type

        if order_no:
            wheres.append(u"order_no like $order_no")
            values["order_no"] = u"%{}%".format(order_no)

        if receiver_phone:
            wheres.append(u"receiver_phone like $receiver_phone")
            values["receiver_phone"] = u"%{}%".format(receiver_phone)

        if trade_no:
            wheres.append(u"trade_no like $trade_no")
            values["trade_no"] = u"%{}%".format(trade_no)

        if start_time:
            wheres.append(u"o.created_time >= $start_time")
            values["start_time"] = start_time

        if end_time:
            wheres.append(u"o.created_time <= $end_time")
            values["end_time"] = end_time

        if channel_code:
            wheres.append(u"channel_code=$channel_code")
            values["channel_code"] = channel_code

        if supplier_id:
            wheres.append(u"supplier_id=$supplier_id")
            values["supplier_id"] = supplier_id

        where_str = u" and ".join(wheres) if wheres else None

        return where_str, values

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

        where_str, values = AdminOrderDao.__gen_wheres_values(is_show_supplier, **kwargs)
        tables = u'orders as o'
        if not whats:
            whats = u"o.*"

            if is_show_supplier:
                whats += u", sp.fullname as supplier_name"
                tables = [u'orders as o', u"suppliers as sp"]

        results = db.slave.select(
            tables=tables,
            what=whats,
            vars=values,
            where=where_str,
            limit=limit,
            offset=offset,
            order=u"o.created_time DESC"
        )

        # 取待发货的列表商品信息
        new_results = []
        for o in results:
            order_goods = db.slave.select(
                tables=u"order_details",
                what=u"product_spu, goods_image, goods_specs, goods_fullname, quantity",
                where={"order_id": o.id}
            )
            o["goods"] = order_goods
            new_results.append(o)

        return new_results

    @staticmethod
    def get_total_count(**kwargs):
        """
        获取对应的条数 query_type -1代表全部,其他值都是对应的订单状态
        :param kwargs:
        :return:
        """
        where_str, values = AdminOrderDao.__gen_wheres_values(**kwargs)

        counts = db.slave.select(
            tables='orders as o',
            what="count(id) as counts",
            vars=values,
            where=where_str
        ).first().counts

        return counts

    @staticmethod
    def show_order_goods_detail(order_id):
        """
        获得订单和商品详情
        :param order_id: 订单ID
        :return:
        """
        result = db.slave.select(
            what=(u"og.id as order_goods_id, o.id as order_id, og.goods_image, og.goods_specs,"
                  u"og.goods_title,og.quantity,o.price, o.post_fee,o.goods_total_price,o.order_no"),
            tables=[u"order_details as og", u"orders as o"],
            where=u"og.order_id = o.id and o.id=$id", vars={'id': order_id}
        ).first()

        return result

    @staticmethod
    def view_order_goods_by_id(order_goods_id):
        """
        根据订单商品ID查看产品详情
        :param order_goods_id:
        :return:
        """
        result = db.slave.select(
            tables=u"order_details",
            what=u"*",
            where={"id": order_goods_id}
        ).first()

        return result

    @staticmethod
    def get_detail(_id=None, order_no=None):
        """
        获得订单详情
        :param _id: 订单ID
        :param order_no:
        :return:
        """
        where = {}
        if _id is not None:
            where["id"] = _id

        if order_no is not None:
            where["order_no"] = order_no

        result = db.slave.select(what=u"*", tables=u"orders", where=where).first()

        return result

    @staticmethod
    def query_order_goods(order_id):
        """
        查看订单所有的商品
        :param order_id:
        :return:
        """

        result = db.slave.select(tables=u"order_details", what=u"*", where={"order_id": order_id})
        return result

    @staticmethod
    def update(_id=None, order_no=None, status=None):
        """
        修改
        :param _id:
        :param order_no:
        :param status:
        :return:
        """
        set_values = {}
        where = {}

        if status is not None:
            set_values["order_status"] = status

        if _id is not None:
            where["id"] = _id

        if order_no is not None:
            where["order_no"] = order_no

        result = db.master.update('orders', where=where, **set_values)

        return result

    @staticmethod
    def cancel(_id, cancel_code, remark=""):
        """
        订单取消
        :param _id:
        :param cancel_code:
        :param remark:
        :return:
        """
        with db.master.transaction():
            cancel_result = db.master.insert(
                tablename="order_cancels",
                order_id=_id,
                cancel_code=cancel_code,
                cancel_remark=remark
            )
            #  更新订单状态
            order_result = db.master.update(
                tables='orders',
                vars={'id': _id},
                where="id=$id ",
                order_status=OrderStatus.Canceled.value
            )

            return cancel_result

    @staticmethod
    def query_order_invoices(order_id, whats=u"*"):
        """
        查询订单发票信息
        :param order_id:
        :param whats:
        :return:
        """
        result = db.slave.select(
            what=whats,
            tables=u"order_invoices",
            where={"order_id": order_id}
        ).first()

        return result

orders = AdminOrderDao
