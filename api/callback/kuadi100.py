#!/usr/bin/env python
# coding: utf8

import logging
from datetime import datetime

from tornado import gen
from tornado.web import RequestHandler
from tornado.escape import json_decode

from application import motor_client
from dao.expressdao import ExpressDao

from dao.orderdao import AdminOrderDao
from configs.constants.order import OrderStatus
from configs.constants.express import ExpressStatus
from plugins.kuaidi100.express_status import ExpressStatus as KDExpressStatus

logger = logging.getLogger("API")


class KD100CallBack(RequestHandler):
    def data_received(self, chunk):
        pass

    @gen.coroutine
    def post(self, *args, **kwargs):
        db = motor_client["demo"]["express_trace"]
        params = self.request.arguments.get("param")
        logger.info(u"快递100回调数据: {}".format(params))

        for param in params:
            param = json_decode(param)
            current_status = param.get("status")
            message = param.get("message")
            last_result = param.get("lastResult")
            track_number = last_result.get("nu", "0")
            express_info = ExpressDao.query_express(track_number)
            if not express_info:
                self.write({"result": False, "returnCode": "200", "message": u"运单不存在: {}".format(track_number)})
                logger.error(u"快递100回调: 运单号: {} 不存在".format(track_number))
                return
            updated_time = express_info.get("updated_time")
            express_status = express_info.get("status")
            if express_status == ExpressStatus.SIGNED.value:
                self.write({"result": True, "returnCode": "200", "message": u"运单已妥投"})
                logger.info(u"快递100回调: 运单号: {}, 已妥投".format(track_number))
                return
            company = last_result.get("com")
            content_data_list = last_result.get("data")
            status = last_result.get("state")
            if not KDExpressStatus.is_member(status):
                self.write({"result": False, "returnCode": "400", "message": u"状态不识别: {}".format(status)})
                logger.error(u"快递100回调: 运单号: {}, 状态不识别".format(track_number))
                return
            route_list = []
            for content_data in content_data_list:
                try:
                    content_time = datetime.strptime(content_data.get("ftime"), "%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    self.write({"result": False, "returnCode": "400", "message": u"时间格式有误"})
                    logger.error(u"快递100回调: 运单号: {}, 时间格式有误".format(track_number))
                    return
                if content_time > updated_time:
                    content_data["ftime"] = content_time
                    route_list.append(content_data)

            if route_list:
                last_route = sorted(route_list, key=lambda x: x.get('ftime'), reverse=True)[0]
                express_update_time = last_route.get("ftime")
                for route in route_list:
                    if not (yield db.insert({"context": route["context"], "track_number": track_number,
                                             "time": route["ftime"], "company": company})):
                        self.write({"result": False, "returnCode": "500", "message": u"记录存取出错"})
                        logger.error(u"快递100回调: 运单号: {}, 记录存取出错".format(track_number))
                        return
                express_status = ExpressStatus.kd100status_to_express_status("E{}".format(status))
                ExpressDao.express_update_by_id(_id=express_info.get("id"), updated_time=express_update_time,
                                                status=express_status)
                if express_status == ExpressStatus.SIGNED.value:
                    AdminOrderDao.update(order_no=express_info.get("record_value"), status=OrderStatus.Sign.value)
            logger.info(u"快递100回调: 运单号: {}, 成功".format(track_number))
            self.write({"result": True, "returnCode": "200", "message": u"成功"})
