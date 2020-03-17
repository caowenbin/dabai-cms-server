#!/usr/bin/env python
# coding: utf8
__author__ = 'ye shuo'

import sys
from functools import wraps

from tornado.web import RequestHandler, HTTPError

auth_users = {
    "FZ": "sftfqlmlSe2LLorPfOe8S3BT1oiHCXb3V2Rokg0tGr4"
}


class APIBaseHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    def _handle_request_exception(self, e):
        if isinstance(e, HTTPError):
            self.send_error(e.status_code, exc_info=sys.exc_info())
        else:
            self.send_error(500, reason=e.message)


def login_required(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        auth_headers = self.request.headers.get("Authorization", None)
        auth_mode, auth_info = auth_headers.split(" ", 1)

        if auth_mode == "Basic":
            auth_name, auth_password = auth_info.decode("base64").split(":")
            if not auth_password == auth_users.get(auth_name, None):
                self.send_error(401)
        else:
            self.send_error(401, reason=u"验证模式只支持Basic")

        return method(self, *args, **kwargs)

    return wrapper
