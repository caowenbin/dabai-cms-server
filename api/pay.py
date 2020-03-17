#!/usr/bin/env python
# coding: utf8

# from web import database
# import urllib
# import json
# from tornado.web import asynchronous
# from tornado.gen import engine, Task
#
# from libs.app_creater import async_client
# from libs.handlers.base import AsyncBaseHandler


class PayHandler(object):
    def get(self, *args, **kwargs):
        self.write(u"你好：张业硕")

