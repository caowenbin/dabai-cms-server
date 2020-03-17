# coding: utf-8

import random
from cores.webpydb import database

__author__ = 'bin wen'


class DB(object):
    def __init__(self, app=None, **connect_kwargs):
        """

        :param user:
        :param password:
        :param database:
        :param host:
        :param port:
        :param connect_kwargs:
        :return:
        """
        self.app = app
        self.master = None
        self.slave = None
        self.db_config = connect_kwargs.get("db_config", "")
        self.__master_dburl = None
        self.__slave_dburls = None
        self.__maxconnections = 200  # 最大允许连接数量
        self.__mincached = 20  # 启动时开启的空连接数量
        if self.db_config:
            self.__master_dburl = self.db_config["master"]
            self.__slave_dburls = self.db_config.get("slave", [])

        if self.app:
            self.init_app(self.app)

    def init_app(self, app, **connect_kwargs):
        self.db_config = app.config["DB"]
        self.__master_dburl = self.db_config["master"]
        self.__slave_dburls = self.db_config.get("slave", [])
        self.__maxconnections = self.db_config.get("maxconnections", self.__maxconnections)
        self.__mincached = self.db_config.get("mincached", self.__mincached)
        self.init_master()
        self.init_slave()

    def init_master(self):
        self.master = database(dburl=self.__master_dburl,
                               mincached=self.__mincached,
                               maxconnections=self.__maxconnections)

    def init_slave(self):
        slave_count = len(self.__slave_dburls)
        if slave_count == 0:
            if self.master:
                self.slave = self.master
                return
            dburl = self.__master_dburl
        else:
            dburl = self.__slave_dburls[random.randint(0, slave_count - 1)]

        self.slave = database(dburl=dburl,
                              mincached=self.__mincached,
                              maxconnections=self.__maxconnections)

