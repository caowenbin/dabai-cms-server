#!/usr/bin/env python
# coding: utf8
__author__ = 'ye shuo'

from tornado.web import RequestHandler
from base import login_required, APIBaseHandler


class Orders(APIBaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        pass

    @login_required
    def post(self, *args, **kwargs):
        print int(None)
        pass