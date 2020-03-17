# coding: utf-8
import hashlib
import logging
import random
import string

from flask import request
from flask.ext.admin.base import expose

from cores.actions import action
from cores.adminweb import BaseHandler
from dao.supplierdao import suppliers
from extends import csrf
from libs.flask_login import login_required
from utils.helpers import utf8

__author__ = 'bin wen'

_log = logging.getLogger("ADMIN")
_handler_log = logging.getLogger("HANDLER")


class SupplierHandler(BaseHandler):
    """
    供应商列表
    """
    column_list = ("fullname", "short_name", "login_name", "contact_name", "contact_phone",
                   "validity", "last_login_time", "last_login_ip", "updated_time")

    column_labels = {
        "fullname": u"供应商全称",
        "short_name": u"供应商简称",
        "login_name": u"登陆账户",
        "contact_name": u"联系人",
        "contact_phone": u"手机号",
        "validity": u"状态",
        "created_time": u"创建时间",
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
    @expose('/supplier/list.html')
    @login_required
    def list_view(self):
        page = request.args.get('page', 0, type=int)
        login_name = request.args.get("login_name", "")
        fullname = request.args.get("fullname", "")
        contact_name = request.args.get("contact_name", "")
        contact_phone = request.args.get("contact_phone", "")
        query_type = request.args.get("query_type", -1, type=int)
        query_kwargs = dict(
                login_name=login_name,
                fullname=fullname,
                query_type=query_type,
                contact_name=contact_name,
                contact_phone=contact_phone
        )

        def pager_url(p):
            if p is None:
                p = 0

            return self._get_url('.list_view', p, **query_kwargs)

        count = suppliers.get_total_count(**query_kwargs)
        results = []
        num_pages = 0

        if count > 0:
            num_pages = self.gen_total_pages(count)
            if num_pages - 1 < page:
                page -= 1

            offset_value = page * self.page_size
            results = suppliers.query_list(limit=self.page_size, offset=offset_value, **query_kwargs)

        actions, actions_confirmation = self.get_actions_list()
        return_url = self.gen_return_url(".list_view", page=page, **query_kwargs)

        return self.render(
            template="supplier/list.html",
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

    @expose('/supplier/action.html', methods=('POST',))
    @login_required
    def action_view(self):
        return_url = request.form.get("return_url", "")
        return self.handle_action(return_view=return_url)

    @action('disable', u"注销(下架)所选", u"你确定要注销(下架)所选的记录?")
    def action_disable(self, ids):
        try:
            result = suppliers.set_validity(ids, validity=0)
            _handler_log.info(u"[AdminListHandler] batch disable, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[AdminListHandler] batch disable error")

    @action('activate', u"激活(上架)选择", u"你确定要激活所选的记录?")
    def action_activate(self, ids):
        try:
            result = suppliers.set_validity(ids, validity=1)
            _handler_log.info(u"[AdminListHandler] batch activate, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[AdminListHandler] batch activate error.")

    @action('delete', u"删除所选", u"你确定要删除所选的记录?")
    def action_delete(self, ids):
        try:
            result = suppliers.delete(ids)
            _handler_log.info(u"[AdminListHandler] batch delete, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[AdminListHandler] batch delete error")

    @staticmethod
    def get_supplier_pwd():
        s = string.digits + string.letters
        return "".join(random.sample(s, 10))

    @expose('/supplier/create.html', methods=('GET', 'POST'))
    @login_required
    def create_view(self):
        if request.method == "GET":
            return self.render(template="supplier/create.html")
        else:
            req_data = self.gen_arguments
            login_name = req_data.get("login_name")
            contact_phone = req_data.get("contact_phone")
            contact_name = req_data.get("contact_name")
            password = req_data.get("password")
            fullname = req_data.get("fullname")
            short_name = req_data.get("short_name")
            encrypt_pwd = hashlib.sha1(password).hexdigest()
            result = suppliers.save(
                fullname=fullname,
                login_name=login_name,
                contact_name=contact_name,
                contact_phone=contact_phone,
                password=encrypt_pwd,
                short_name=short_name,
                operator=self.current_operator
            )

            return self.make_write(result_code=0, result_data=self.reverse_url(".list_view"))

    @expose('/supplier/edit.html', methods=('GET', 'POST'))
    @login_required
    def edit_view(self):
        if request.method == "GET":
            _id = request.args.get("id", "")
            return_url = request.args.get("return_url", "")
            result = suppliers.get_detail(_id=_id)

            return self.render(
                    template="supplier/edit.html",
                    data=result,
                    return_url=return_url
            )
        else:
            req_data = self.gen_arguments
            return_url = req_data.get("return_url", "")
            _id = req_data.get("id")
            new_password = req_data.get("new_password")
            fullname = req_data.get("fullname", "")
            contact_name = req_data.get("contact_name", "")
            contact_phone = req_data.get("contact_phone", "")
            short_name = req_data.get("short_name", "")

            encrypt_pwd = hashlib.sha1(new_password).hexdigest() if new_password else None

            result = suppliers.update(
                _id=_id,
                password=encrypt_pwd,
                fullname=fullname,
                contact_name=contact_name,
                contact_phone=contact_phone,
                short_name=short_name,
                operator=self.current_operator
            )

            return self.make_write(result_code=0, result_data=self.decode_return_url(return_url))

    @expose('/supplier/delete.html', methods=('POST',))
    @login_required
    def delete_view(self):
        req_data = self.gen_arguments
        return_url = req_data.get("return_url", "")
        _id = req_data.get("id")
        result = suppliers.delete([_id])

        _handler_log.exception(u"[AdminDeleteHandler] admin_id:{}, operator: {}".format(
                utf8(_id), self.current_operator))

        return self.make_write(result_code=0, result_data=self.decode_return_url(return_url))

    @expose('/supplier/detail.html', methods=('GET',))
    @login_required
    def detail_view(self):
        _id = request.args.get("id", "")
        return_url = request.args.get("return_url", "")
        result = suppliers.get_detail(_id=_id)
        return self.render(
                template="supplier/detail.html",
                data=result,
                return_url=self.decode_return_url(return_url)
        )

    @csrf.exempt
    @expose('/supplier/ajax/check.html', methods=('POST',))
    def check_view(self):
        login_name = request.data.get("login_name")
        supplier_info = suppliers.get_detail(whats="id", login_name=login_name)
        result_code = 102 if supplier_info else 0

        return self.make_write(result_code=result_code)
