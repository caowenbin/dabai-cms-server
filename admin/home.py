# coding: utf-8
import hashlib

from flask import request

from cores.adminweb import BaseHandler
from flask.ext.admin import expose

from dao.admindao import admin
from dao.supplierdao import suppliers
from libs.flask_login import login_required

__author__ = 'bin wen'


class HomeHandler(BaseHandler):
    """
    个人中心
    """
    @expose('/')
    @expose("/home.html")
    @login_required
    def home(self):
        """
        个人中心
        :return:
        """
        return self.render('index.html')

    @expose("/pwd/edit.html", methods=("GET", "POST"))
    @login_required
    def edit_pwd(self):
        """
        登录密码服务
        :return:
        """
        if request.method == "GET":
            return self.render("pwd.html")
        else:
            req_data = self.gen_arguments
            old_password = req_data.get("old_password")
            new_password = req_data.get("new_password")
            user_model = req_data.get("user_model")
            user_id = req_data.get("user_id")

            if not old_password or not new_password:
                return self.make_write(result_code=1005)

            if user_model == "admin":
                user_info = admin.get_detail(whats="id, password", _id=user_id)
                update_model = admin
            elif user_model == "supplier":
                user_info = suppliers.get_detail(whats="id, password", _id=user_id)
                update_model = suppliers
            else:
                return self.make_write(result_code=100)

            if not user_info:
                return self.make_write(result_code=1006)

            encrypt_old_pwd = hashlib.sha1(old_password).hexdigest()
            if encrypt_old_pwd != user_info.password:
                return self.make_write(result_code=1006)

            encrypt_pwd = hashlib.sha1(new_password).hexdigest()
            result = update_model.update(_id=user_id, password=encrypt_pwd)

            return self.make_write(result_code=0, result_data="")

