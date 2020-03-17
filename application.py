# coding:utf-8
import logging

from flask import Flask, url_for

from configs.settings import SETTINGS
from extends import cache, mongo, db, admin, csrf, login_manager, qn, kd100
from libs.logger import init_logger_handler
from urls.adminurls import init_admin_url

__author__ = 'bin wen'


class Application(Flask):

    def __init__(self, service="all", env="default"):
        super(Application, self).__init__(import_name=env)
        self.register_request_listener()
        self.init_settings()
        self.init_extends()
        self.init_api_url()
        self.init_log()

    def init_settings(self):
        """
        初始化配置文件及加载支付平台的密钥信息
        :return:
        """
        self.config.from_object(SETTINGS[self.name])
        self.jinja_env.globals.update(static_url=self.static_url)

    def init_extends(self):
        """
        初始化扩展
        :return:
        """
        cache.init_app(app=self, config={'CACHE_TYPE': 'simple'})
        mongo.init_app(app=self)
        db.init_app(app=self)
        login_manager.init_app(app=self)
        admin.init_app(app=self)
        csrf.init_app(app=self)

        qn.init_app(self)
        kd100.init_app(self)

    def init_api_url(self):
        """
        加载url
        :return:
        """
        init_admin_url(app=self)

    def register_request_listener(self):
        """
        注册每一个请求绑定一个函数,包括请求之前、请求之后
        """

        @self.teardown_request
        def teardown_request(response_or_exc):
            """
            每一个请求之后绑定一个函数，即使遇到了异常
            :param response_or_exc:
            :return:
            """
            if isinstance(response_or_exc, BaseException):
                try:
                    self.logger.exception(response_or_exc.message)
                except BaseException, e:
                    self.logger.error(e.message)

            return response_or_exc

    @staticmethod
    def static_url(path):
        """
        静态文件
        :param path:
        :return:
        """
        return url_for("static", filename=path)

    def init_log(self):
        """
        初始化日志
        :return:
        """
        logs_path = self.config["LOGS_PATH"]

        admin_logger = logging.getLogger("ADMIN")
        admin_logger.setLevel(logging.INFO)
        admin_logger.addHandler(init_logger_handler(logs_path))

        api_logger = logging.getLogger("API")
        api_logger.setLevel(logging.INFO)
        api_logger.addHandler(init_logger_handler(logs_path))

        action_logger = logging.getLogger("HANDLER")
        action_logger.setLevel(logging.INFO)
        action_logger.addHandler(init_logger_handler(logs_path, file_name="handler_note"))
#
