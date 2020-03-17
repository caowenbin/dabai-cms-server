# coding: utf-8
from baseenum import Enum, constant_doc

__author__ = 'bin wen'


@constant_doc
class PayModel(Enum):
    """
    支付方式
    """
    PlaneYeePay = u"易宝支付(离线)"
    OnlineYeePay = u"易宝支付(在线)"
    UnionPOSPay = u"刷卡支付(银联)"
    YMInPay = u"现金支付"
    WebWxPay = u"微信支付(WEB)"
    AppWxPay = u"微信支付(APP)"
    WebAliPay = u"支付宝(WEB)"
    AppAliPay = u"支付宝(APP)"

    @classmethod
    def list(cls):
        return [{"name": status.value, "value": status.name} for status in cls]