# #!/usr/bin/env python
# # coding: utf8
# __author__ = 'ye shuo'
#
# from application import ccelery
# from base import DefaultTask
#
#
# @ccelery.task(name="sync_express_to_kd100", base=DefaultTask, bind=True)
# def sync_express_to_kd100(self, track_number, express_code, *args, **kwargs):
#     if not track_number or not express_code:
#         return u"参数不合法"
#
#     data = {
#         "company": express_code,
#         "number": track_number
#     }
#     self.logger.info(u"同步运单: {} 到快递100".format(data))
#     response = self.kd100.send(data)
#     self.logger.info(u"同步到快递100返回: {} ,运单号: {}".format(response, track_number))
