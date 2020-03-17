# coding: utf-8
from flask import request
from flask.ext.admin import expose

from cores.adminweb import BaseHandler
from utils.function_data_flow import flow_tools

__author__ = 'bin wen'


class ContentSelectHandler(BaseHandler):
    """
    模板内容下拉框
    """

    @expose('/')
    @expose('/content_select/list.html')
    def list_view(self):
        content_type = int(request.args.get("content_type", 0))
        req_page = request.args.get("req_page", "group_template")
        if content_type == 0:
            select_content_list = list(flow_tools.gen_bind_products())
        elif req_page in ("banner", "group_template") and content_type in (1, 2):
            select_content_list = flow_tools.gen_bind_tweets()
        elif req_page == "banner" and content_type == 3:
            select_content_list = flow_tools.gen_bind_groups()
        return self.make_write(result_code=0, result_data=select_content_list)
