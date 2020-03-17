# coding: utf-8
import hashlib
import logging

from flask import request
from flask.ext.admin import expose

from cores.actions import action
from cores.adminweb import BaseHandler
from dao.admindao import admin
from extends import csrf
from libs.flask_login import login_required
from utils.helpers import utf8

__author__ = 'bin wen'

_log = logging.getLogger("ADMIN")
_handler_log = logging.getLogger("HANDLER")


class AdministratorsHandler(BaseHandler):
    """
    管理员列表
    """
    column_list = ("email", "fullname", "administer", "validity", "last_login_time",
                   "last_login_ip", "updated_time")

    column_labels = {
        "email": u"登录邮箱",
        "fullname": u"真实姓名",
        "administer": u"是否管理员",
        "validity": u"状态",
        "updated_time": u"变更时间",
        "last_login_time": u"上次登录时间",
        "last_login_ip": u"上次登录IP"
    }
    column_widget_args = {
        "last_login_ip": {'class': "hidden-480"},
        "last_login_time": {'class': "hidden-480"}
    }
    tabs_list = (
        {"query_type": -1, "name": u"全部"},
        {"query_type": 1, "name": u"可登录"},
        {"query_type": 0, "name": u"已注销"}
    )

    @expose('/')
    @expose('/list.html')
    @login_required
    def list_view(self):
        page = request.args.get('page', 0, type=int)
        email = request.args.get('email', "")
        fullname = request.args.get('fullname', '')
        query_type = request.args.get('query_type', -1, type=int)

        query_kwargs = dict(email=email, fullname=fullname, query_type=query_type)

        def pager_url(p):
            if p is None:
                p = 0

            return self._get_url('.list_view', p, **query_kwargs)

        count = admin.get_total_count(
                query_type=query_type,
                email=email,
                fullname=fullname
        )

        results = []
        num_pages = 0

        if count > 0:
            num_pages = self.gen_total_pages(count)
            if num_pages - 1 < page:
                page -= 1

            offset_value = page * self.page_size
            results = admin.query_list(
                    query_type=query_type,
                    email=email,
                    fullname=fullname,
                    limit=self.page_size,
                    offset=offset_value
            )

        actions, actions_confirmation = self.get_actions_list()
        return_url = self.gen_return_url(".list_view", page=page, **query_kwargs)

        return self.render(
            template="admin/list.html",
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

    @expose('/action.html', methods=('POST',))
    @login_required
    def action_view(self):
        return_url = request.form.get("return_url", "")
        return self.handle_action(return_view=return_url)

    @action('disable', u"注销(下架)所选", u"你确定要注销(下架)所选的记录?")
    def action_disable(self, ids):
        try:
            result = admin.set_validity(ids, validity=0)
            _handler_log.info(u"[AdminListHandler] batch disable, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[AdminListHandler] batch disable error")

    @action('activate', u"激活(上架)选择", u"你确定要激活所选的记录?")
    def action_activate(self, ids):
        try:
            result = admin.set_validity(ids, validity=1)
            _handler_log.info(u"[AdminListHandler] batch activate, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[AdminListHandler] batch activate error.")

    @action('delete', u"删除所选", u"你确定要删除所选的记录?")
    def action_delete(self, ids):
        try:
            result = admin.delete(*ids)
            _handler_log.info(u"[AdminListHandler] batch delete, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[AdminListHandler] batch delete error")

    @expose('/create.html', methods=('GET', 'POST'))
    @login_required
    def create_view(self):
        if request.method == "GET":
            breadcrumb = (
                {"name": u"管理员配置", "url": ".list_view"},
                {"name": u"新增管理员", "url": ".create_view"}
            )
            return self.render(template="admin/create.html", breadcrumb=breadcrumb)
        else:
            req_data = self.gen_arguments
            login_email = req_data.get("login_email", "")
            password = req_data.get("password", "")
            fullname = req_data.get("fullname", "")
            is_admin = req_data.get("is_admin", "off")
            admin_info = admin.get_detail(whats="id", login_name=login_email)
            if admin_info:
                return self.make_write(result_code=102, result_msg=u"该邮件已经注册了")

            encrypt_pwd = hashlib.sha1(password).hexdigest()
            result = admin.save(
                    email=login_email,
                    password=encrypt_pwd,
                    fullname=fullname,
                    is_admin=1 if is_admin == "on" else 0
            )

            _handler_log.exception((u"[AdminCreateHandler] login_email:{}, is_admin:{}, "
                                    u"operator: {}".format(utf8(login_email),
                                                           utf8(is_admin),
                                                           self.current_operator))
                                   )

            return self.make_write(result_code=0, result_data=self.reverse_url(".list_view"))

    @expose('/edit.html', methods=('GET', 'POST'))
    @login_required
    def edit_view(self):
        if request.method == "GET":
            _id = request.args.get("id", "")
            return_url = request.args.get("return_url", "")
            result = admin.get_detail(_id=_id)
            return self.render(
                    template="admin/edit.html",
                    data=result,
                    return_url=return_url
            )
        else:
            req_data = self.gen_arguments
            return_url = req_data.get("return_url", "")
            _id = req_data.get("id")
            new_password = req_data.get("new_password")
            fullname = req_data.get("fullname", "")
            is_admin = req_data.get("is_admin", "off")

            encrypt_pwd = hashlib.sha1(new_password).hexdigest() if new_password else None

            result = admin.update(
                    _id=_id,
                    password=encrypt_pwd,
                    fullname=fullname,
                    is_admin=1 if is_admin == "on" else 0
            )

            _handler_log.exception((u"[AdminEditHandler] admin_id:{}, is_admin:{}, "
                                    u"operator: {}".format(utf8(_id),  utf8(is_admin),
                                                           self.current_operator))
                                   )

            return self.make_write(result_code=0, result_data=self.decode_return_url(return_url))

    @expose('/delete.html', methods=('POST',))
    @login_required
    def delete_view(self):
        req_data = self.gen_arguments
        return_url = req_data.get("return_url", "")
        _id = req_data.get("id")
        result = admin.delete(_id)

        _handler_log.exception(u"[AdminDeleteHandler] admin_id:{}, operator: {}".format(
                utf8(_id), self.current_operator))

        return self.make_write(result_code=0, result_data=self.decode_return_url(return_url))

    @expose('/detail.html', methods=('GET',))
    @login_required
    def detail_view(self):
        _id = request.args.get("id", "")
        return_url = request.args.get("return_url", "")
        result = admin.get_detail(_id=_id)
        return self.render(
                template="admin/detail.html",
                data=result,
                return_url=self.decode_return_url(return_url)
        )

    @csrf.exempt
    @expose('/ajax/check.html', methods=('POST',))
    def check_view(self):
        req_data = self.gen_arguments
        login_email = req_data.get("login_email")
        if not login_email:
            return self.make_write(result_code=102)

        admin_info = admin.get_detail(whats="id", login_name=login_email)
        result_code = 102 if admin_info else 0

        return self.make_write(result_code=result_code)
