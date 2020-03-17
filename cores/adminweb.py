# coding: utf-8
import base64
import urllib

from flask import request, redirect, url_for, session
from flask import jsonify
from flask.ext.admin import BaseView
from werkzeug.utils import cached_property

from configs.resultcodes import RESULT_CODES
from cores.actions import ActionsMixin

__author__ = 'bin wen'


class BaseHandler(BaseView, ActionsMixin):
    page_size = 10

    def __init__(self, name=None, endpoint="admin", url="/admin", menu_icon_value=None, is_menu=True):
        self.is_menu = is_menu
        super(BaseHandler, self).__init__(name=name, endpoint=endpoint, url=url, menu_icon_value=menu_icon_value)
        self.init_actions()

    @staticmethod
    def make_write(result_code, result_data=None, result_msg=None):
        """
        生成返回信息
        :param result_code:
        :param result_data:
        :param result_msg:
        :return:
        """
        msg = result_msg
        if not msg:
            msg = RESULT_CODES.get(result_code, "")

        result = {"code": result_code, "msg": msg}
        if result_data is not None:
            result["data"] = result_data
        return jsonify(**result)

    @staticmethod
    def write(result_data):
        """
        直接返回
        :param result_data:
        :return:
        """
        return jsonify(result_data)

    @staticmethod
    def reverse_url(endpoint, **values):
        """
        生成对应的url
        :param endpoint:
        :param values:
        :return:
        """
        return url_for(endpoint, **values)

    @staticmethod
    def redirect(location, code=302):
        """
        重定向
        :param location:
        :param code:
        :return:
        """
        return redirect(location, code=code)

    @property
    def gen_arguments(self):
        """
        取得请求参数
        :return:
        """
        req_json = request.json
        req_data = request.date
        req_form = request.form
        print req_json, req_data, req_form
        if req_json:
            return req_json
        if req_data:
            return req_data
        if req_form:
            return req_form

    def _get_url(self, url_name, p, **kwargs):
        """
        生成分页url
        :param url_name: url命名空间名
        :param p: 页码
        :param kwargs: 参数
        :return:
        """
        if p is None:
            p = 0

        kwargs["page"] = p
        url = self.reverse_url(url_name)
        for k, v in kwargs.iteritems():
            if isinstance(v, unicode):
                v = v.encode("utf-8")
                kwargs[k] = v
        return u"{}?{}".format(url, urllib.urlencode(kwargs))

    def gen_return_url(self, url_name, **kwargs):
        """
        生成跳转的url
        :param url_name:
        :param kwargs:
        :return:
        """
        url = self.reverse_url(url_name)
        for k, v in kwargs.iteritems():
            if isinstance(v, unicode):
                v = v.encode("utf-8")
                kwargs[k] = v
        return_url = base64.urlsafe_b64encode(u"{}?{}".format(url, urllib.urlencode(kwargs)))
        return return_url

    @staticmethod
    def decode_return_url(url):
        """
        解开url
        :param url:
        :return:
        """
        if isinstance(url, unicode):
            url = str(url)
        return_url = base64.urlsafe_b64decode(url)
        return return_url

    def gen_total_pages(self, count):
        """
        总页数
        :param count:
        :return:
        """
        num_pages = count // self.page_size
        if count % self.page_size != 0:
            num_pages += 1

        return num_pages

    def handle_action(self, return_view=None):
        """
            Handle action request.

            :param return_view:
                Name of the view to return to after the request.
                If not provided, will return user to the index view.
        """
        action = request.form.get('action')
        ids = request.form.getlist('rowid')

        handler = self._actions_data.get(action)

        if handler and self.is_action_allowed(action):
            response = handler[0](ids)

            # if response is not None:
            #     return response

        return self.redirect(self.decode_return_url(return_view))

    @cached_property
    def current_operator(self):
        """
        当前的操作者
        :return:
        """
        return session.get("operator", u"system")
