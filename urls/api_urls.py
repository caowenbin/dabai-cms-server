#!/usr/bin/env python
# coding: utf8

from api.pay import PayHandler
from api.orders import Orders
from api.callback.kuadi100 import KD100CallBack

url_patterns = [(r"/pay", PayHandler), (r"/callback/kuaidi100", KD100CallBack), (r"/orders", Orders)]