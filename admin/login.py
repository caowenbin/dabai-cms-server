# coding: utf-8
import hashlib

from flask import request, session
from flask.ext.admin import expose

from cores.storage import storage
from dao.admindao import admin
from dao.supplierdao import suppliers
from extends import login_manager
from cores.adminweb import BaseHandler
from libs.flask_login import login_user, logout_user

__author__ = 'bin wen'


@login_manager.user_loader
def load_user(user_id, user_model):
    if not user_id or user_model is None:
        return None

    user = storage(
        name=session.get("name", ""),
        operator=session.get("operator", ""),
        user_id=session.get("user_id", 0),
        user_model=session.get("user_model", ""),
        is_active=True if session.get("is_active", 0) in (1, "1") else False,
        is_authenticated=True
    )
    return user


class LoginOutHandler(BaseHandler):
    """
    用户登录与退出
    """

    @expose("/", methods=("GET", "POST"))
    @expose("/login.html", methods=("GET", "POST"))
    def login(self):
        if request.method == "GET":
            return self.render("login.html")
        else:
            req_data = self.gen_arguments
            login_name = req_data.get("login_name", "")
            password = req_data.get("password", "")
            user_model = req_data.get("user_model")
            remote_ip = request.access_route[0]

            if not login_name or not password:
                return self.make_write(result_code=1002)

            if user_model == "admin":
                user_info = admin.get_detail(
                        whats="id, password, fullname, administer, validity",
                        login_name=login_name,
                        confirmed=1
                )
                update_model = admin
            elif user_model == "supplier":
                user_info = suppliers.get_detail(
                        whats="id, password, fullname, validity",
                        login_name=login_name
                )
                update_model = suppliers
            else:
                return self.make_write(result_code=100)

            if not user_info:
                return self.make_write(result_code=1003)

            if user_info.validity == 0:
                return self.make_write(result_code=1004)

            encrypt_pwd = hashlib.sha1(password).hexdigest()
            if encrypt_pwd != user_info.password:
                return self.make_write(result_code=1003)

            user = storage(
                name=user_info.fullname,
                operator=login_name,
                user_id=user_info.id,
                user_model=user_model,
                is_active=user_info.validity
            )
            login_user(user)
            if update_model is not None:
                result = update_model.update(_id=user_info.id, remote_ip=remote_ip)

            return self.make_write(result_code=0, result_data=self.reverse_url("home.home"))

    @expose("/logout.html", methods=("GET",))
    def logout(self):
        logout_user()
        return self.redirect(self.reverse_url("auth.login"))
