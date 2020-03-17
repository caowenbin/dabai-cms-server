#!/usr/bin/env python
# coding: utf8
__author__ = 'ye shuo'

from requests import request


class SyncCmsClient(object):
    def __init__(self, url=None):
        self.url = url

    def init_app(self, app):
        self.url = app.settings["cms_url"]

    def _request(self, method, data):
        url_path = self.url

        response = request(method, url_path, data=data)
        return response.json()

    def sync(self, data):
        return self._request("POST", data)