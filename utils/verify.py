# coding: utf-8
import re

__author__ = 'bin wen'


class VerifyData(object):
    """
    数据校对中心
    """

    @staticmethod
    def check_mobile(mobile):
        """
        检查手机格式
        :param mobile:
        :return:
        """
        pattern = re.compile(ur'^(13\d|14[57]|15[^4,\D]|17[678]|18\d)\d{8}|170[059]\d{7}$')
        m = pattern.search(mobile)
        if not m:
            return False
        return True

    @staticmethod
    def check_name(name):
        """
        检查名称格式, 1-20位
        :param name:
        :return:
        """
        pattern = re.compile(ur'^[\w\u4e00-\u9fa5\s]{1,20}$')
        m = pattern.search(name)
        if not m:
            return False
        return True

    @staticmethod
    def check_number(number):
        """
        检查数字
        :param number:
        :return:
        """
        pattern = re.compile(ur'^[1-9]\d*$')
        m = pattern.search(number)
        if not m:
            return False
        return True

    @staticmethod
    def check_email(email):
        """
        检查邮箱(公司邮箱)
        :param email:
        :return:
        """
        #pattern = re.compile(ur'[\S+]{1,16}@cicaero.com$')
        pattern = re.compile(ur'^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$')
        m = pattern.search(email)
        if not m:
            return False
        return True

    @staticmethod
    def check_login_name(login_name):
        """
        检查登录帐号(只能输入8-20个以字母开头、可带数字、“_”、“.”的字串)
        :param login_name:
        :return:
        """
        pattern = re.compile(ur'^[a-zA-Z]{1}([a-zA-Z0-9]|[._]){7,30}$')
        m = pattern.search(login_name)
        if not m:
            return False
        return True

verify = VerifyData
