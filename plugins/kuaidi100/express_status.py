#!/usr/bin/env python
# coding: utf8
__author__ = 'ye shuo'

from enum import Enum


class ExpressStatus(Enum):
    E0 = u"在途"
    E1 = u"揽件"
    E2 = u"疑难"
    E3 = u"签收"
    E4 = u"退签"
    E5 = u"派件"
    E6 = u"退回"

    @classmethod
    def is_member(cls, data):
        m = cls.__members__.get("E{}".format(data))
        if m:
            return True
        return False
