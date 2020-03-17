# coding: utf-8
from dateutils import gen_number_time
from random import randint
__author__ = 'bin wen'


class NumberingUnit(object):
    """
    生成各种编号
    """

    @staticmethod
    def gen_refund_no():
        """
        生成退款订单号
        格式:退款标记(3)+ 年差(年份减2016基数)+月日时分秒+4位随机数,比如3005200909094567,共16位
        :return:
        """
        number = "3{time}{rand_value}".format(time=gen_number_time(), rand_value=randint(1000, 9999))
        return number

    @staticmethod
    def gen_banner_code():
        """
        生成焦点图编码
        b+年差(年份减2016基数)+月日时分秒+3位随机数,比如b00520090909457,共15位
        :return:
        """
        number = "b{time}{rand_value}".format(time=gen_number_time(), rand_value=randint(100, 999))
        return number


numbers = NumberingUnit
