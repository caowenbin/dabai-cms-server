#!/usr/bin/env python
# coding: utf8

import datetime
import time

month_code = [hex(i).replace('0x', '').upper() for i in xrange(1, 13)]


def year_letter():
    return datetime.date.today().year - 2016


def month_letter():
    return month_code[datetime.date.today().month - 1]


def current_datetime_as_str(format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(format)


def current_datetime():
    return datetime.datetime.now()


def datetime2str(datetime,format="%Y-%m-%d %H:%M:%S"):
    return datetime.strftime(format)


def str2datetime(datetime_str,format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.strptime(datetime_str,format)


def current_timestampms():
    return int(time.time()*1000)


def current_timestamps():
    return int(time.time())


def timestampms2datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp/float(1000))


def datetime2timestampms(datetime):
    return int(time.mktime(datetime.timetuple())*1000)


def timestampms2datetimestr(timestampms,format="%Y-%m-%d %H:%M:%S"):
    return datetime2str(timestampms2datetime(timestampms), format)


def gen_number_time():
    """
    生成编码中的时间值
    :return:
    """
    now_time = datetime.datetime.now()
    year = now_time.year - 2016
    mdhms = now_time.strftime("%m%d%H%M%S")
    number_time = u"{}{}".format(year, mdhms)

    return number_time