# coding: utf-8
from flask.ext.cache import Cache
from flask.ext.pymongo import PyMongo
from flask.ext.wtf import CsrfProtect

from cores.db import DB
from libs.admin_base import Admin
from libs.flask_login import LoginManager
from plugins.kuaidi100.client import KuaiDi100Client
from plugins.qiniu.client import QiNiuClient

__author__ = 'bin wen'
# #######  flask扩展    ######
cache = Cache()
mongo = PyMongo()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
admin = Admin()
csrf = CsrfProtect()

# ######  内部封装的  #####
db = DB()
qn = QiNiuClient()
kd100 = KuaiDi100Client()
