# coding: utf-8
import logging

from flask import request
from flask.ext.admin import expose

from cores.actions import action
from cores.adminweb import BaseHandler
from dao.bannerdao import banner
from extends import csrf
from libs.flask_login import login_required
from utils.function_data_flow import flow_tools
from utils.helpers import utf8
from utils.numbering import numbers

__author__ = 'bin wen'

_log = logging.getLogger("ADMIN")
_handler_log = logging.getLogger("HANDLER")


class BannerHandler(BaseHandler):
    """
    轮播焦点图列表
    """
    column_list = ("banner_code", "name", "banner_type", "target", "image", 'validity',
                   "updated_time", "remark")

    column_labels = {
        "banner_code": u"编号",
        "name": u"名称",
        "banner_type": u"类型",
        "target": u"跳转目标",
        "image": u"图片",
        "validity": u"状态",
        "updated_time": u"变更时间",
        "remark": u"备注"
    }
    column_widget_args = {
        "image": {'class': "hidden-480"},
        "remark": {'class': "hidden-480"}
    }
    tabs_list = (
        {"query_type": -1, "name": u"全部"},
        {"query_type": 1, "name": u"有效的"},
        {"query_type": 0, "name": u"已作废"}
    )

    @expose('/')
    @expose('/banner/list.html')
    @login_required
    def list_view(self):
        page = request.args.get('page', 0, type=int)
        name = request.args.get('name', "")
        query_type = request.args.get('query_type', -1, type=int)

        query_kwargs = dict(name=name, query_type=query_type)

        def pager_url(p):
            if p is None:
                p = 0

            return self._get_url('.list_view', p, **query_kwargs)

        count = banner.get_total_count(**query_kwargs)

        results = []
        num_pages = 0

        if count > 0:
            num_pages = self.gen_total_pages(count)
            if num_pages - 1 < page:
                page -= 1

            offset_value = page * self.page_size
            results = banner.query_list(
                    query_type=query_type,
                    name=name,
                    limit=self.page_size,
                    offset=offset_value
            )

        actions, actions_confirmation = self.get_actions_list()
        return_url = self.gen_return_url(".list_view", page=page, **query_kwargs)

        return self.render(
            template="banner/list.html",
            actions=actions,
            actions_confirmation=actions_confirmation,
            count=count,
            page=page,
            num_pages=num_pages,
            pager_url=pager_url,
            data=results,
            query_kwargs=query_kwargs,
            return_url=return_url,
            column_list=self.column_list,
            column_labels=self.column_labels,
            column_widget_args=self.column_widget_args,
            tabs_list=self.tabs_list,
            banner_types=flow_tools.gen_banner_type()
        )

    @expose('/banner/action.html', methods=('POST',))
    @login_required
    def action_view(self):
        return_url = request.form.get("return_url", "")
        return self.handle_action(return_view=return_url)

    @action('disable', u"注销(下架)所选", u"你确定要注销(下架)所选的记录?")
    def action_disable(self, ids):
        try:
            result = banner.set_validity(ids, validity=0)
            _handler_log.info(u"[BannerListHandler] batch disable, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[BannerListHandler] batch disable error")

    @action('activate', u"激活(上架)选择", u"你确定要激活所选的记录?")
    def action_activate(self, ids):
        try:
            result = banner.set_validity(ids, validity=1)
            _handler_log.info(u"[BannerListHandler] batch disable, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[BannerListHandler] batch disable error")

    @action('delete', u"删除所选", u"你确定要删除所选的记录?")
    def action_delete(self, ids):
        try:
            result = banner.delete(ids)
            _handler_log.info(u"[BannerListHandler] batch delete, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[BannerListHandler] batch delete error")

    @expose('/banner/create.html', methods=('GET', 'POST'))
    @login_required
    def create_view(self):
        if request.method == "GET":
            select_content_list = flow_tools.gen_bind_products()
            result = {
                "select_content_list": select_content_list,
                "banner_types": flow_tools.gen_banner_type()
            }
            return self.render(template="banner/create.html", data=result)
        else:
            req_data = self.gen_arguments
            name = req_data.get("name")
            banner_type = int(req_data.get("banner_type", 0))
            url_target = req_data.get("url_target", "")  # 外部url
            select_target = req_data.get("select_target", "")  # 下拉内容
            remark = req_data.get("remark", "")
            picture_url_list = req_data.getlist("picture_url")  # 图片url
            if not picture_url_list:
                return self.make_write(result_code=4002)

            if banner_type == 2:
                target = url_target
            else:
                target = select_target
            result = banner.save(
                banner_code=numbers.gen_banner_code(),
                name=name,
                banner_type=banner_type,
                target=target,
                image_url=picture_url_list[0],
                remark=remark
            )

            return self.make_write(result_code=0, result_data=self.reverse_url(".list_view"))

    @expose('/banner/edit.html', methods=('GET', 'POST'))
    @login_required
    def edit_view(self):
        if request.method == "GET":
            _id = request.args.get("id", "")
            return_url = request.args.get("return_url", "")
            result = banner.get_detail(_id)
            banner_type = result.banner_type
            select_content_list = []
            if banner_type == 0:
                select_content_list = flow_tools.gen_bind_products()
            elif banner_type == 1:
                select_content_list = flow_tools.gen_bind_tweets()
            elif banner_type == 3:
                select_content_list = flow_tools.gen_bind_groups()

            result["banner_types"] = flow_tools.gen_banner_type()
            result["select_content_list"] = select_content_list

            return self.render(
                    template="banner/edit.html",
                    data=result,
                    return_url=return_url
            )
        else:
            req_data = self.gen_arguments
            return_url = req_data.get("return_url", "")

            _id = req_data.get("id")
            name = req_data.get("name")
            banner_type = int(req_data.get("banner_type", 0))
            url_target = req_data.get("url_target", "")  # 外部url
            select_target = req_data.get("select_target", "")  # 下拉内容
            remark = req_data.get("remark", "")
            picture_url_list = req_data.getlist("picture_url")  # 图片url
            if not picture_url_list:
                return self.make_write(result_code=4002)

            if banner_type == 2:
                target = url_target
            else:
                target = select_target

            result = banner.update(
                    _id=_id,
                    name=name,
                    banner_type=banner_type,
                    target=target,
                    image_url=picture_url_list[0],
                    remark=remark
            )

            return self.make_write(result_code=0, result_data=self.decode_return_url(return_url))

    @expose('/banner/delete.html', methods=('POST',))
    @login_required
    def delete_view(self):
        req_data = self.gen_arguments
        return_url = req_data.get("return_url", "")
        _id = req_data.get("id")
        result = banner.delete([_id])

        _handler_log.exception(u"[AdminDeleteHandler] admin_id:{}, operator: {}".format(
                utf8(_id), self.current_operator))

        return self.make_write(result_code=0, result_data=self.decode_return_url(return_url))

    @expose('/banner/detail.html', methods=('GET',))
    @login_required
    def detail_view(self):
        pass

    @csrf.exempt
    @expose('/banner/ajax/check.html', methods=('POST',))
    def check_view(self):
        pass

