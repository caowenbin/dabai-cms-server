#!/usr/bin/env python
# coding: utf8

import six
import random
import string
from configs.resultcodes import RESULT_CODES


def text(string):
    if isinstance(string, six.text_type):
        return string.encode('utf8')
    elif isinstance(string, six.binary_type):
        return string
    else:
        return six.text_type(string).encode('utf8')


def utf8(string):
    if isinstance(string, six.text_type):
        return string
    elif isinstance(string, six.binary_type):
        return string.decode('utf8')
    else:
        return six.text_type(string)


def find_in(find, from_):
    found = False
    for f in find:
        if from_.find(f) >= 0:
            found = True
            break

    return found


def toint(value):
    try:
        return int(value)
    except:
        pass
    return value


def make_code_msg(code):
    return RESULT_CODES.get(code, "")


if __name__ == "__main__":
    print utf8("hello word"), type(utf8("hello word"))
    print text(u"你好"), type(text(u'你好'))