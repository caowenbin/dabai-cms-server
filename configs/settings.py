# coding:utf-8
import os

import datetime

__author__ = 'bin wen'

curdir = os.getcwd()


class Config(object):
    # 设置调试模式, 默认为False，即不是调试模式
    DEBUG = False
    # 设置templates路径
    TEMPLATE_PATH = os.path.join(curdir, "templates")
    # 设置静态文件解析路径
    STATIC_PATH = os.path.join(curdir, "static")
    # 设置防跨站请求攻击, 默认为False，即不可防御
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'a random string'
    # 设置登陆路径，未登陆用户在操作时跳转会用到这个参数
    # login_url = "/login.html"

    # 设置gzip压缩
    # gzip = True
    # 设置静态路径头部, 默认是"/static/"
    # static_url_prefix = "/static/"

    # ########  session缓存配置 #######
    # session key
    SECRET_KEY = "binbin"
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=20)
    # 会话保护
    SESSION_PROTECTION = "strong"

    # ##########  主从库 从库可以配置多个,用";"隔开###########
    slave_databases = os.environ.get('slave_db', '')
    DB = {
        "master": os.environ.get('master_db', "mysql://root:@127.0.0.1:3306/pop"),
        "slave": [s for s in slave_databases.split(";") if s],
    }

    # 七牛配置
    QINIU = {
        "access_key": "",
        "secret_key": "",
        "bucket_name": "test-demo",
        "qn_domain_name": ""
    }

    # 快递100P配置
    KD100 = {
        "url": "",
        "key": "",
        "callback_url": ""
    }

    # #######  日志目录 #########
    LOGS_PATH = curdir+'/logs'

    # #####  上传媒体路径 ####
    UPLOAD_MEDIAS_FOLDER = curdir+"/medias"


class LocalConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    debug = False
    qiniu = {
        "access_key": "",
        "secret_key": "",
        "bucket_name": "",
        "qn_domain_name": ""
    }


class StagingConfig(Config):
    debug = False


SETTINGS = {
    'production': ProductionConfig,
    'default': LocalConfig,
    'staging': StagingConfig
}
