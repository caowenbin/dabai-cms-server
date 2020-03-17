#!/usr/bin/env python
# coding: utf8
from baseenum import Enum, constant_doc
__author__ = 'ye shuo'


@constant_doc
class OrderStatus(Enum):
    """
    订单状态
    """
    ToBePaid = 0  # 待支付
    ToBeVerification = 1  # 待验证
    Paid = 2  # 已支付
    Shipped = 3  # 已发货
    Sign = 4  # 已签收
    Canceled = 5  # 已取消
    Refunded = 6  # 已退款

    @classmethod
    def list(cls):
        return [{"name": status.name, "value": status.value } for status in cls]


@constant_doc
class CancelStatus(Enum):
    """
    取消订单原因
    """
    DoNotBuy = "OC001"  # 不买了
    InformationError = "OC002"  # 信息错误
    OutStock = "OC003"  # 卖家缺货
    Other = "OC004"  # 其他原因

    @classmethod
    def list(cls):
        return [{"name": status.name, "value": status.value} for status in cls]


