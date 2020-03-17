# coding: utf-8
import enum
__author__ = 'bin wen'

CONSTANTS = {}


def constant_doc(cls):
    name = cls.__name__.lower()
    if name not in CONSTANTS:
        CONSTANTS[name] = cls
    return cls


class Enum(enum.Enum):
    @classmethod
    def names(cls):
        return [c.name for c in cls]

    @classmethod
    def values(cls):
        return [c.value for c in cls]

    @classmethod
    def get_value_by_name(cls, name, default=None):
        """
        根据key获得value
        :param name: key的值
        :param default:
        :return:
        """
        m = cls.__members__.get(name)

        if m:
            return m.value

        return default

    @classmethod
    def get_name_by_value(cls, value, default=None):
        """
        根据value获得name
        :param value: value
        :param default:
        :return:
        """
        for i in cls:
            if i.value == value:
                return i.name

        return default
