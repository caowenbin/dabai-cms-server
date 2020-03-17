#!/usr/bin/env python
# coding: utf8
from baseenum import Enum, constant_doc

from plugins.kuaidi100.express_status import ExpressStatus as KDExpressStatus

__author__ = 'ye shuo'


@constant_doc
class ExpressNumberRecordType(Enum):
    """
    快递单号记录的对应的记录类型
    """
    ORDER = 0  # 订单发货单
    REFUND = 1  # 退款发货单


@constant_doc
class ExpressStatus(Enum):
    """
    :type Created: enum
    :type Confirmed: enum
    :type SeekGoods: enum
    :type DISPATCHING: enum
    :type SIGNED: enum
    :type EXCEPT_CANCEL: enum
    :type CANCEL: enum
    """
    Created = 0  # 运单创建
    Confirmed = 1  # 运单确认
    SeekGoods = 2  # 揽件
    DISPATCHING = 3  # 在途
    SIGNED = 4  # 签收
    CANCEL = 5  # 取消
    EXCEPT_CANCEL = 6  # 异常

    @classmethod
    def kd100status_to_express_status(cls, kd100_status):
        if kd100_status in [KDExpressStatus.E0.name]:
            return cls.Confirmed.value
        if kd100_status in [KDExpressStatus.E1.name]:
            return cls.SeekGoods.value
        if kd100_status in [KDExpressStatus.E5.name]:
            return cls.DISPATCHING.value
        if kd100_status in [KDExpressStatus.E3.name]:
            return cls.SIGNED.value
        if kd100_status in [KDExpressStatus.E2.name, KDExpressStatus.E4.name, KDExpressStatus.E6.name]:
            return cls.EXCEPT_CANCEL.value


@constant_doc
class ExpressCompany(Enum):
    """
    快递公司
    """
    SF = "shunfeng"  # 顺丰
    ST = "shentong"  # 申通
    YT = "yuantong"  # 圆通
    ZT = "zhongtong"  # 中通
    HTKD = "huitongkuaidi"  # 汇通
    YD = "yunda"  # 韵达
    ZJS = "zhaijisong"  # 宅急送
    TT = "tiantian"  # 天天
    DBWL = "debangwuliu"  # 德邦
    YZ = "youzhengguonei"  # 邮政包裹/平邮
    EMS = "ems"  # EMS
    EMS_JI = "emsguoji"  # EMS-国际件
    EMS_BJ = "emsguoji"  # 北京EMS
    GT = "guotongkuaidi"  # 国通
    ZTKY = "ztky"  # 中铁物流
    ZTWL = "zhongtiewuliu"  # 中铁快运
    QFKD = "quanfengkuaidi"  # 全峰
    JD = "jd"  # 京东
    RFD = "rufengda"  # 如风达

    @classmethod
    def list(cls):
        return [{"name": status.name, "value": status.value} for status in cls]