# coding: utf-8
import logging

from flask import request
from flask.ext.admin import expose

from configs.constants.express import ExpressNumberRecordType
from cores.adminweb import BaseHandler
from dao.expressdao import express
from dao.orderdao import orders
# from tasks.sync_express_to_kd100 import sync_express_to_kd100
from libs.flask_login import login_required

__author__ = 'bin wen'

_log = logging.getLogger("ADMIN")
_handler_log = logging.getLogger("HANDLER")


class OrderHandler(BaseHandler):
    """
    订单列表
    """

    column_list = ("order_detail", "receiver_detail", "price", "order_status", "remarks")

    column_labels = {
        "order_no": u"订单编号",
        "receiver_phone": u"收货人手机号",
        "receiver": u"收件人姓名",
        "receiver_address": u"收货地址",
        "created_time": u"下单时间",
        "pay_time": u"支付时间",
        "channel_code": u"下单渠道",
        "buyer_phone": u"下单人手机号",
        "order_status": u"状态",
        "updated_time": u"变更时间",
        "price": u"订单金额",
        "supplier_name": u"供应商",
        "order_detail": u"订单详情",
        "receiver_detail": u"收货人",
        "remarks": u"客户备注"
    }
    column_widget_args = {
        "pay_time": {'class': "hidden-480"},
        "channel_code": {'class': "hidden-480"},
        "buyer_phone": {'class': "hidden-480"},
        "order_status": {'class': "hidden-480"},
        "updated_time": {'class': "hidden-480"},
        "price": {'class': "hidden-480 width-150"},
        "order_detail": {'class': "width-450"},
        "receiver_detail": {'class': "width-200"},
    }
    tabs_list = (
        {"query_type": -1, "name": u"全部"},
        {"query_type": 0, "name": u"待支付"},
        {"query_type": 1, "name": u"待验证"},
        {"query_type": 2, "name": u"待发货"},
        {"query_type": 3, "name": u"待签收"},
        {"query_type": 4, "name": u"已签收"},
        {"query_type": 5, "name": u"已取消"},
    )

    @expose('/')
    @expose('/order/list.html')
    @login_required
    def list_view(self):
        page = request.args.get('page', 0, type=int)
        order_no = request.args.get("order_no", "")
        receiver_phone = request.args.get("receiver_phone", "")
        trade_no = request.args.get("trade_no", "")
        start_time = request.args.get("start_time", "")
        end_time = request.args.get("end_time", "")
        channel_code = request.args.get("channel_code", "")
        user_model = self.session["user"]["user_model"]
        if user_model == "admin":
            supplier_id = request.args.get("supplier_id", "")
            query_type = request.args.get("query_type", -1, type=int)
        else:
            supplier_id = self.session["user"]["id"]
            query_type = request.args.get("query_type", 2, type=int)

        query_kwargs = dict(
                order_no=order_no,
                receiver_phone=receiver_phone,
                trade_no=trade_no,
                start_time=start_time,
                end_time=end_time,
                channel_code=channel_code,
                supplier_id=supplier_id,
                query_type=query_type
        )

        def pager_url(p):
            if p is None:
                p = 0

            return self._get_url('.list_view', p, **query_kwargs)

        count = orders.get_total_count(**query_kwargs)

        results = []
        num_pages = 0

        if count > 0:
            num_pages = self.gen_total_pages(count)
            if num_pages - 1 < page:
                page -= 1

            offset_value = page * self.page_size
            results = orders.query_list(limit=self.page_size, offset=offset_value, **query_kwargs)

        actions, actions_confirmation = self.get_actions_list()
        return_url = self.gen_return_url(".list_view", page=page, **query_kwargs)

        return self.render(
            template="order/list.html",
            actions=actions,
            actions_confirmation=actions_confirmation,
            count=count,
            page=page,
            num_pages=num_pages,
            pager_url=pager_url,
            data=results,
            query_kwargs=query_kwargs,
            return_url=return_url,
            column_list=self.column_list,
            column_labels=self.column_labels,
            column_widget_args=self.column_widget_args,
            tabs_list=self.tabs_list
        )

    @staticmethod
    def show_basic_info(order_no):
        """
        查看基本信息
        :param order_no:
        :return:
        """
        result = orders.get_detail(order_no=order_no)
        return result

    @staticmethod
    def show_order_goods(order_id):
        """
        查看商品信息
        :param order_id:
        :return:
        """
        result = orders.query_order_goods(order_id=order_id)
        return result

    @staticmethod
    def show_express_info(order_no):
        """
        查看物流信息
        :param order_no:
        :return:
        """
        express_info = express.show_express_detail(
            record_type=ExpressNumberRecordType.ORDER.value,
            record_value=order_no,
        )

        return express_info

    @expose('/order/detail.html', methods=('GET',))
    @login_required
    def detail_view(self):
        order_id = request.args.get("id", "")
        return_url = request.args.get("return_url", "")
        order_no = request.args.get("order_no", "")
        query_type = request.args.get("query_type", 0, type=int)
        query_kwargs = dict(query_type=query_type, order_no=order_no, order_id=order_id)
        results = {}
        if query_type == 2:
            results = self.show_express_info(order_no=order_no)
        if query_type == 0:
            results = self.show_basic_info(order_no=order_no)
        if query_type == 1:
            results = self.show_order_goods(order_id=order_id)

        return self.render(
                template="order/detail.html",
                query_kwargs=query_kwargs,
                results=results,
                back_url=self.decode_return_url(return_url),
                return_url=return_url
        )

    @expose('/order/send.html', methods=('GET', "POST"))
    @login_required
    def order_send_view(self):
        """
        订单发货
        :return:
        """
        if request.method == "GET":
            order_no = request.args.get("tid")
            _id = request.args.get("id")
            data = {"order_no": order_no,
                    "id": _id,
                    "return_url": request.args.get("return_url", "")
                    }
            return self.render(template="order/send_order.html", data=data)
        else:
            req_data = request.user_agent
            track_no = req_data.get("track_no")
            order_no = req_data.get("order_no")
            express_code = req_data.get("express_code")
            return_url = req_data.get("return_url", "")

            result = express.save(record_type=0,
                                  record_value=order_no,
                                  track_no=track_no,
                                  express_code=express_code
                                  )
            if result:
                try:
                    pass
                    # 同步订单到快递100
                    # sync_express_to_kd100.apply_async(args=[track_no, express_code])
                except Exception, e:
                    _log.exception(u"[OrderSendHandler] sync express to kd100 error.")

            _url = self.decode_return_url(return_url) if return_url else self.reverse_url(".list_view")
            return self.make_write(result_code=0, result_data=_url)

    @expose('/order/cancel.html', methods=('GET', "POST"))
    @login_required
    def order_cancel_view(self):
        """
        订单取消
        :return:
        """
        if request.method == "GET":
            order_no = request.args.get("tid")
            _id = request.args.get("id")
            data = {"order_no": order_no,
                    "id": _id,
                    "return_url": request.args.get("return_url", "")
                    }
            return self.render(template="order/cancel_order.html", data=data)
        else:
            req_data = request.user_agent
            order_id = req_data.get("id")
            cancel_code = req_data.get("cancel_code")
            remark = req_data.get("remark")
            return_url = req_data.get("return_url", "")

            result = orders.cancel(order_id, cancel_code, remark)  # 记录订单取消原因
            _url = self.decode_return_url(return_url) if return_url else self.reverse_url(".list_view")
            return self.make_write(result_code=0, result_data=_url)
