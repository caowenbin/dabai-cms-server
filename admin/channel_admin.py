# coding: utf-8
import logging

from flask import request
from flask.ext.admin import expose

from cores.actions import action
from cores.adminweb import BaseHandler
from dao.channeldao import channel
from extends import csrf
from libs.flask_login import login_required
from utils.helpers import utf8

__author__ = 'bin wen'

_log = logging.getLogger("ADMIN")
_handler_log = logging.getLogger("HANDLER")


class ChannelHandler(BaseHandler):
    """
    渠道列表
    """
    column_list = ("channel_code", "name", "secret_key", "validity", "updated_time",  "remarks")

    column_labels = {
        "name": u"渠道名称",
        "channel_code": u"真实姓名",
        "secret_key": u"通信密钥",
        "validity": u"状态",
        "updated_time": u"变更时间",
        "remarks": u"备注",
    }
    column_widget_args = {
        "remarks": {'class': "hidden-480"},
    }
    tabs_list = (
        {"query_type": -1, "name": u"全部"},
        {"query_type": 1, "name": u"合作中"},
        {"query_type": 0, "name": u"已注销"}
    )

    @expose('/')
    @expose('/channel/list.html')
    @login_required
    def list_view(self):
        page = request.args.get('page', 0, type=int)
        name = request.args.get('name', "")
        channel_code = request.args.get('channel_code', '')
        query_type = request.args.get('query_type', -1, type=int)

        query_kwargs = dict(name=name, channel_code=channel_code, query_type=query_type)

        def pager_url(p):
            if p is None:
                p = 0

            return self._get_url('.list_view', p, **query_kwargs)

        count = channel.get_total_count(query_type=query_type, name=name, channel_code=channel_code)

        results = []
        num_pages = 0

        if count > 0:
            num_pages = self.gen_total_pages(count)
            if num_pages - 1 < page:
                page -= 1

            offset_value = page * self.page_size
            results = channel.query_list(
                    query_type=query_type,
                    name=name,
                    channel_code=channel_code,
                    limit=self.page_size,
                    offset=offset_value
            )

        actions, actions_confirmation = self.get_actions_list()
        return_url = self.gen_return_url(".list_view", page=page, **query_kwargs)

        return self.render(
            template="channel/list.html",
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

    @expose('/channel/action.html', methods=('POST',))
    @login_required
    def action_view(self):
        return_url = request.form.get("return_url", "")
        return self.handle_action(return_view=return_url)

    @action('disable', u"注销(下架)所选", u"你确定要注销(下架)所选的记录?")
    def action_disable(self, ids):
        try:
            result = channel.set_validity(ids, validity=0)
            _handler_log.info(u"[AdminListHandler] batch disable, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[AdminListHandler] batch disable error")

    @action('activate', u"激活(上架)选择", u"你确定要激活所选的记录?")
    def action_activate(self, ids):
        try:
            result = channel.set_validity(ids, validity=1)
            _handler_log.info(u"[AdminListHandler] batch activate, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[AdminListHandler] batch activate error.")

    @action('delete', u"删除所选", u"你确定要删除所选的记录?")
    def action_delete(self, ids):
        try:
            result = channel.delete(ids)
            _handler_log.info(u"[AdminListHandler] batch delete, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[AdminListHandler] batch delete error")

    @expose('/channel/create.html', methods=('GET', 'POST'))
    @login_required
    def create_view(self):
        if request.method == "GET":
            return self.render(template="channel/create.html")
        else:
            req_data = self.gen_arguments
            name = req_data.get("name", "")
            remarks = req_data.get("remarks", "")
            secret_key = req_data.get("secret_key", "")
            channel_code = req_data.get("channel_code", "")

            result = channel.save(channel_code=channel_code, name=name, remarks=remarks, secret_key=secret_key)

            return self.make_write(result_code=0, result_data=self.reverse_url(".list_view"))

    @expose('/channel/edit.html', methods=('GET', 'POST'))
    @login_required
    def edit_view(self):
        if request.method == "GET":
            _id = request.args.get("id", "")
            return_url = request.args.get("return_url", "")
            result = channel.get_detail(_id=_id)
            return self.render(
                    template="channel/edit.html",
                    data=result,
                    return_url=return_url
            )
        else:
            req_data = self.gen_arguments
            return_url = req_data.get("return_url", "")
            _id = req_data.get("id")
            name = req_data.get("name", "")
            remarks = req_data.get("remarks", "")
            secret_key = req_data.get("secret_key", "")

            result = channel.update(_id=_id, name=name, remarks=remarks, secret_key=secret_key)
            return self.make_write(result_code=0, result_data=self.decode_return_url(return_url))

    @expose('/channel/delete.html', methods=('POST',))
    @login_required
    def delete_view(self):
        req_data = self.gen_arguments
        return_url = req_data.get("return_url", "")
        _id = req_data.get("id")
        result = channel.delete([_id])

        _handler_log.exception(u"[AdminDeleteHandler] admin_id:{}, operator: {}".format(
                utf8(_id), self.current_operator))

        return self.make_write(result_code=0, result_data=self.decode_return_url(return_url))

    @expose('/channel/detail.html', methods=('GET',))
    @login_required
    def detail_view(self):
        pass

    @csrf.exempt
    @expose('/channel/ajax/check.html', methods=('POST',))
    def check_view(self):
        pass
