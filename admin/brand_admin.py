# coding: utf-8
import logging

from flask import request
from flask.ext.admin import expose

from cores.actions import action
from cores.adminweb import BaseHandler
from dao.branddao import brands
from extends import csrf
from libs.flask_login import login_required
from utils.helpers import utf8

__author__ = 'bin wen'

_log = logging.getLogger("ADMIN")
_handler_log = logging.getLogger("HANDLER")


class BrandHandler(BaseHandler):
    """
    品牌列表
    """
    column_list = ("name", "created_time", "updated_time")

    column_labels = {
        "name": u"品牌名称",
        "created_time": u"创建时间",
        "updated_time": u"变更时间"
    }
    column_widget_args = {}
    tabs_list = (
        {"query_type": -1, "name": u"全部"},
    )

    @expose('/')
    @expose('/brand/list.html')
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

        count = brands.get_total_count(name=name)

        results = []
        num_pages = 0

        if count > 0:
            num_pages = self.gen_total_pages(count)
            if num_pages - 1 < page:
                page -= 1

            offset_value = page * self.page_size
            results = brands.query_list(name=name, limit=self.page_size, offset=offset_value)

        actions, actions_confirmation = self.get_actions_list()
        return_url = self.gen_return_url(".list_view", page=page, **query_kwargs)

        return self.render(
            template="brand/list.html",
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
            tabs_list=self.tabs_list
        )

    @expose('/brand/action.html', methods=('POST',))
    @login_required
    def action_view(self):
        return_url = request.form.get("return_url", "")
        return self.handle_action(return_view=return_url)

    @action('delete', u"删除所选", u"你确定要删除所选的记录?")
    def action_delete(self, ids):
        try:
            result = brands.delete(ids)
            _handler_log.info(u"[AdminListHandler] batch delete, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[AdminListHandler] batch delete error")

    @expose('/brand/create.html', methods=('GET', 'POST'))
    @login_required
    def create_view(self):
        if request.method == "GET":
            return self.render(template="brand/create.html")
        else:
            req_data = self.gen_arguments
            name = req_data.get("name", "")
            result = brands.save(name=name)

            return self.make_write(result_code=0, result_data=self.reverse_url(".list_view"))

    @expose('/brand/edit.html', methods=('GET', 'POST'))
    @login_required
    def edit_view(self):
        pass

    @expose('/brand/delete.html', methods=('POST',))
    @login_required
    def delete_view(self):
        req_data = self.gen_arguments
        return_url = req_data.get("return_url", "")
        _id = req_data.get("id")
        result = brands.delete([_id])

        _handler_log.exception(u"[AdminDeleteHandler] admin_id:{}, operator: {}".format(
                utf8(_id), self.current_operator))

        return self.make_write(result_code=0, result_data=self.decode_return_url(return_url))

    @expose('/brand/detail.html', methods=('GET',))
    @login_required
    def detail_view(self):
        pass

    @csrf.exempt
    @expose('/brand/ajax/check.html', methods=('POST',))
    def check_view(self):
        pass
