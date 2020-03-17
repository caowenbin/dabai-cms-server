# coding: utf-8
from exceptions import StandardError

__author__ = 'bin wen'


class BaseError(StandardError):
    """Base Error"""


class ConfigError(BaseError):
    """raise config error"""
