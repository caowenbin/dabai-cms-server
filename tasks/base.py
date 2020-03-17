#!/usr/bin/env python
# coding: utf8
__author__ = 'ye shuo'

import os
import logging

from celery import Task

from cores.config import Config
from configs.settings import SETTINGS
from utils.helpers import get_root_path
from libs.logger import init_logger_handler
from plugins.kuaidi100.client import KuaiDi100Client


class DefaultTask(Task):

    __kd100 = None
    __config = None
    __logger = None

    def run(self, *args, **kwargs):
        raise NotImplementedError('Tasks must define the run method.')

    @property
    def config(self):
        if self.__config is None:
            env = os.environ.get('EC_ENV', 'default')
            self.__config = Config(get_root_path(env), dict(debug=False))
            self.__config.from_object(SETTINGS[env])

        return self.__config

    @property
    def logger(self):
        if self.__logger is None:
            self.__logger = logging.getLogger("API")
            self.__logger.setLevel(logging.INFO)
            self.__logger.addHandler(init_logger_handler(self.config["logs_path"]))

        return self.__logger

    @property
    def kd100(self):
        if self.__kd100 is None:
            self.__kd100 = KuaiDi100Client(self.config["kd100_key"],
                                           self.config["kd100_url"],
                                           self.config["kd100_callback"])

        return self.__kd100
