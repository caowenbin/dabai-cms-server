#!/usr/bin/env python
# coding: utf8
from baseenum import Enum, constant_doc
__author__ = 'ye shuo'


@constant_doc
class RefundReason(Enum):
    """
    退款原因
    """
    ProductInformationError = 0  # 商品信息描述不符
    Wrong = 1  # 错发
    LessOrMissing = 2  # 少件/漏发
    PackingOrProductDamaged = 3  # 包装/商品破损
    NotDeliverInAppointedTime = 4  # 未按约定时间发货
    NotReceiverPackage = 5  # 快递/物流一直未送到
    Other = 6  # 其他

    @classmethod
    def list(cls):
        return [{"name": status.name, "value": "{}".format(status.value)} for status in cls]


@constant_doc
class RefundStatus(Enum):
    """
    退款状态
    """
    WaitCustomerServiceConfirm = 0  # 退款协议等待客服确认
    CustomerServiceRefuseWaitBuyerEdit = 1  # 客服不同意退款协议，等待买家修改
    WaitSellerConfirm = 2  # 退款协议等待卖家确认
    SellerRefuseWaitBuyerEdit = 3  # 卖家不同意退款协议，等待买家修改
    RefundAgreeWaitBuyerReturn = 4  # 退款协议达成，等待买家退货
    BuyerReturnWaitSellerConfirm = 5  # 买家已退货，等待卖家确认收货
    WaitFinancialAudit = 9  # 等待财务审核
    RefundInProcess = 10  # 退款处理中
    RefundSuccess = 11  # 退款成功
    RefundClose = 12  # 退款关闭

    @classmethod
    def list(cls):
        return [{"name": status.name, "value": status.value}
                for status in cls if status.value not in (2, 3)
                ]


@constant_doc
class CloseRefundReason(Enum):
    """
    关闭退款原因
    """
    BuyerCloseRefund = 0  # 买家关闭退款
    SellerCloseRefund = 1  # 卖家关闭退款
    FinancialReject = 2  # 财务驳回
    RefundException = 3  # 退款异常
    Other = 4  # 其他

    @classmethod
    def list(cls):
        return [{"name": status.name, "value": status.value } for status in cls]
