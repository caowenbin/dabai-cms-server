#!/usr/bin/env python
# coding: utf8
import logging
from requests import request

from utils.helpers import json_encode

__author__ = 'ye shuo'

logger = logging.getLogger("API")


class KuaiDi100Client(object):
    def __init__(self, key="", url="", callback=""):
        self.key = key
        self.url = url
        self.callback = callback

    def init_app(self, app):
        _config = app.config["KD100"]
        self.url = _config["url"]
        self.key = _config["key"]
        self.callback = _config["callback_url"]

    def _request(self, method, data):
        url_path = self.url.rstrip("/")

        kwargs = {
            "schema": "json",
            "param": json_encode(data)
        }
        logger.info(u"请求快递100 url: {} -- 参数: {}".format(url_path, kwargs))
        response = request(method, url_path, data=kwargs)
        logger.info(u"快递100返回: {}".format(response.text))
        return response.json()

    def send(self, data):
        data.update({
            "key": self.key,
            "parameters": {
                "callbackurl": self.callback
            }
        })

        result = self._request("POST", data)
        return result


