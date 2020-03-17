# coding: utf-8
from flask import request
from flask.ext.admin import expose

from dao.expressdao import express
from dao.orderdao import orders
from libs.flask_login import login_required
from utils.numbering import numbers
from dao.refunddao import refund
from dao.supplierdao import suppliers
from cores.adminweb import BaseHandler
from configs.constants.refund import RefundStatus
from configs.constants.express import ExpressNumberRecordType

__author__ = 'bin wen'


class RefundHandler(BaseHandler):
    """
    退款管理列表
    """
    column_list = ("created_time", "order_no", "refund_no", "refund_fee", "refund_status",
                   "refund_reason_code", "supplier_name")

    column_labels = {
        "order_no": u"订单编号",
        "refund_no": u"退款单号",
        "refund_fee": u"退款金额",
        "refund_status": u"退款状态",
        "refund_reason_code": u"退款原因",
        "supplier_name": u"供应商",
        "remarks": u"客户备注",
        "created_time": u"申请时间",
    }
    column_widget_args = {}
    tabs_list = (
        {"query_type": -1, "name": u"全部"},
        {"query_type": 4, "name": u"等待买家退货"},
        {"query_type": 5, "name": u"等待卖家确认收货"},
        {"query_type": 9, "name": u"等待财务审核"},
        {"query_type": 10, "name": u"退款处理中"},
        {"query_type": 11, "name": u"退款成功"},
        {"query_type": 12, "name": u"退款关闭"}
    )

    page_size = 20

    @expose('/')
    @expose('/refund/list.html')
    @login_required
    def list_view(self):
        page = request.args.get('page', 0, type=int)
        order_no = request.args.get("order_no", "")
        start_time = request.args.get("start_time", "")
        end_time = request.args.get("end_time", "")
        refund_status = request.args.get("refund_status", "")
        user_model = self.session["user"]["user_model"]
        if user_model == "admin":
            supplier_id = request.args.get("supplier_id", "")
            query_type = int(request.args.get("query_type", -1))
            column_list = self.column_list
        else:
            supplier_id = self.session["user"]["id"]
            query_type = int(request.args.get("query_type", 5))
            column_list = ("created_time", "order_no", "refund_no", "refund_fee", "refund_status",
                           "refund_reason_code")

        query_kwargs = dict(
            order_no=order_no,
            start_time=start_time,
            end_time=end_time,
            supplier_id=supplier_id,
            query_type=query_type,
            refund_status=refund_status
        )

        def pager_url(p):
            if p is None:
                p = 0

            return self._get_url('.list_view', p, **query_kwargs)

        count = refund.get_total_count(**query_kwargs)

        results = []
        num_pages = 0

        if count > 0:
            num_pages = self.gen_total_pages(count)
            if num_pages - 1 < page:
                page -= 1

            offset_value = page * self.page_size
            results = refund.query_list(limit=self.page_size, offset=offset_value, **query_kwargs)

        return_url = self.gen_return_url("refund", page=page, **query_kwargs)
        _supplier_list = []
        if user_model == "admin":
            _supplier_list = suppliers.query_list(whats=u"id, fullname as name")  # 获取供应商

        return self.render(
            template="list.html",
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
            tabs_list=self.tabs_list,
            suppliers=_supplier_list
        )

    @staticmethod
    def gen_refund_info(order_details):
        """
        :param order_details: 订单商品数据
        :return: 退款结构数据
        """
        return {
            "order_id": order_details.get("id"),
            "order_no": order_details.get("order_no"),
            "pay_trade_no": order_details.get("trade_no"),
            "refund_type": order_details.get("pay_type"),
            "supplier_id": order_details.get("supplier_id"),
            "channel_code": order_details.get("channel_code"),
            "refund_no": numbers.gen_refund_no()  # 生成退款订单号
        }

    @expose('/refund/apply.html', methods=('GET', 'POST'))
    @login_required
    def apply_refund_view(self):
        """
        申请退款
        :return:
        """
        if request.method == "GET":
            order_id = request.args.get("id")
            return_url = request.args.get("return_url", "")
            order_details = orders.show_order_goods_detail(order_id=order_id)
            back_url = self.decode_return_url(return_url) if return_url else self.reverse_url("order.list_view")
            return self.render(
                    template="refund/refund.html",
                    data=order_details,
                    return_url=return_url,
                    back_url=back_url
            )
        else:
            req_data = self.gen_arguments
            order_goods_id = req_data.get("order_goods_id")
            order_id = req_data.get("order_id")
            refund_reason = req_data.get("refund_reason")
            remark = req_data.get("remark", "")
            picture_urls = req_data.getlis("picture_url", [])
            order_details = orders.get_detail(_id=order_id)
            refund_fee = float(req_data.get("refund_fee", 0)) * 100
            return_url = req_data.get("return_url", "")

            refund_data = self.gen_refund_info(order_details)
            refund_data["order_goods_id"] = order_goods_id
            refund_data["refund_reason_code"] = refund_reason
            refund_data["remark"] = remark
            refund_data["refund_fee"] = refund_fee
            refund_data["operator"] = self.session["operator"]
            refund_data["refund_status"] = RefundStatus.RefundAgreeWaitBuyerReturn.value

            result = refund.save(picture_urls, **refund_data)
            return_url = self.decode_return_url(return_url) if return_url else self.reverse_url("order.list_view")
            return self.make_write(result_code=0, result_data=return_url)

    @expose('/refund/detail.html', methods=('GET',))
    @login_required
    def detail_view(self):
        refund_id = request.args.get("id")
        refund_info = refund.get_detail(_id=refund_id)
        refund_evidences = refund.query_refund_evidences(refund_id=refund_id)
        refund_goods = orders.view_order_goods_by_id(order_goods_id=refund_info.order_goods_id)
        refund_express = None
        if refund_info.refund_status >= 5:
            refund_express = express.show_express_detail(
                    record_value=refund_info.refund_no,
                    record_type=ExpressNumberRecordType.REFUND.value
            )
        return_url = request.args.get("return_url", "")

        data = {"refund_info": refund_info,
                "refund_evidences": refund_evidences,
                "refund_goods": refund_goods,
                "refund_express": refund_express
                }
        return self.render(
                template="refund/view.html",
                data=data,
                back_url=self.decode_return_url(return_url),
                return_url=return_url
        )

    @expose('/refund/close.html', methods=('POST',))
    @login_required
    def refund_close_view(self):
        """
        关闭退款
        :return:
        """
        refund_id = request.args.get("id")
        current_status = refund.get_detail(_id=refund_id, whats=u"refund_status").refund_status

        if current_status >= 10:
            return self.make_write(result_code=6001)
        result = refund.update(
                _id=refund_id,
                wheres={"refund_status": current_status},
                status=RefundStatus.RefundClose.value
        )
        return self.make_write(result_code=0, result_data=self.reverse_url(".list_view"))

    @staticmethod
    def treasurer(refund_id):
        """
        财务审核
        :param refund_id:
        :return:
        """
        result = refund.update(_id=refund_id, status=RefundStatus.RefundInProcess.value)
        return result

    @staticmethod
    def custom_audit_pass(refund_id):
        """
        客服审核通过
        :param refund_id:
        :return:
        """
        result = refund.update(_id=refund_id, status=RefundStatus.RefundAgreeWaitBuyerReturn.value)
        return result

    @staticmethod
    def custom_audit_fail(refund_id):
        """
        客服审核不通过
        :param refund_id:
        :return:
        """
        result = refund.update(_id=refund_id, status=RefundStatus.CustomerServiceRefuseWaitBuyerEdit.value)
        return result

    @expose('/refund/agree.html', methods=('POST',))
    @login_required
    def post(self):
        agree_data = request.form.get("id", "").split("-")  # 格式 退款申请ID-状态码
        refund_id = agree_data[0]
        current_status = int(agree_data[1])
        if current_status == 4:
            result = self.treasurer(refund_id=refund_id)
        elif current_status == 0:
            result = self.treasurer(refund_id=refund_id)
        elif current_status == 3:
            result = self.treasurer(refund_id=refund_id)

        return self.make_write(result_code=0, result_data=self.reverse_url(".list_view"))

    @expose('/refund/append/info.html', methods=('GET', 'POST'))
    @login_required
    def refund_append_info(self):
        """
        追加退款信息
        :return:
        """
        if request.method == "GET":
            refund_id = request.args.get("id")
            refund_info = refund.get_detail(_id=refund_id)
            return_url = request.args.get("return_url", "")
            refund_evidences = refund.query_refund_evidences(refund_id=refund_id)
            order_details = orders.show_order_goods_detail(order_id=refund_info.order_id)
            data = {"refund_info": refund_info,
                    "order_details": order_details,
                    "refund_evidences": refund_evidences
                    }
            return self.render(
                    template="refund/append_refund_info.html",
                    data=data,
                    return_url=return_url
            )
        else:
            req_data = self.gen_arguments
            refund_id = req_data.get("id")
            refund_reason = req_data.get("refund_reason")
            remark = req_data.get("remark", "")
            picture_urls = req_data.getlist("picture_url", [])
            order_price = int(req_data.get("order_price"))
            refund_fee = float(req_data.get("refund_fee", 0)) * 100
            return_url = req_data.get("return_url", "")
            if refund_fee > order_price:
                return self.make_write(result_code=6002)

            refund_data = dict(refund_reason_code=refund_reason, remark=remark, refund_fee=refund_fee)
            result = refund.update(_id=refund_id, picture_urls=picture_urls, **refund_data)
            return_url = self.decode_return_url(return_url) if return_url else self.reverse_url("order")
            return self.make_write(result_code=0, result_data=return_url)

    @expose('/refund/express.html', methods=('GET', 'POST'))
    @login_required
    def refund_express(self):
        """
        退货运单
        :return:
        """
        if request.method == "GET":
            refund_no = request.args.get("refund_no")
            data = {"refund_no": refund_no,
                    "return_url": request.args.get("return_url", "")
                    }
            return self.render(template="refund/express.html", data=data)
        else:
            req_data = self.gen_arguments
            track_no = req_data.get("track_no")
            refund_no = req_data.get("refund_no")
            express_code = req_data.get("express_code")
            return_url = req_data.get("return_url", "")

            result = express.save(record_type=1,
                                  record_value=refund_no,
                                  track_no=track_no,
                                  express_code=express_code
                                  )
            _url = self.decode_return_url(return_url) if return_url else self.reverse_url(".list_view")
            return self.make_write(result_code=0, result_data=_url)

    @expose('/refund/express/sign.html', methods=('GET', 'POST'))
    @login_required
    def refund_express_sign(self):
        """
        退货运单签收,即确认收货
        :return:
        """
        if request.method == "GET":
            refund_id = request.args.get("id")
            refund_info = refund.get_detail(
                _id=refund_id,
                whats=u"id, refund_no, order_id, order_no, order_goods_id, refund_reason_code, remark"
            )
            refund_express = express.show_express_detail(
                record_value=refund_info.refund_no,
                record_type=ExpressNumberRecordType.REFUND.value
            )
            order_invoice = orders.query_order_invoices(order_id=refund_info.order_id, whats=u"id")
            refund_goods = orders.view_order_goods_by_id(order_goods_id=refund_info.order_goods_id)

            data = {"refund_info": refund_info,
                    "refund_express": refund_express,
                    "order_invoice": order_invoice,
                    "refund_goods": refund_goods,
                    "return_url": request.args.get("return_url", "")
                    }
            return self.render(template="refund/sign.html", data=data)
        else:
            req_data = self.gen_arguments
            _id = req_data.get("id")
            sign_invoice = req_data.get("sign_invoice", "0")
            return_url = req_data.get("return_url", "")
            sign_goods = req_data.get("sign_goods", None)
            if not sign_goods:
                return self.make_write(result_code=6003)

            result = refund.update(
                _id=_id,
                return_invoice=sign_invoice,
                status=RefundStatus.WaitFinancialAudit.value
            )
            _url = self.decode_return_url(return_url) if return_url else self.reverse_url(".list_view")
            return self.make_write(result_code=0, result_data=_url)
