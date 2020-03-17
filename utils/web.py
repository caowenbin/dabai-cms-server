# coding: utf-8
from flask import jsonify, request

from configs.resultcodes import RESULT_CODES

__author__ = 'bin wen'


def make_write(result_code, result_data=None, result_msg=None):
    """
    生成返回信息
    :param result_code:
    :param result_data:
    :param result_msg:
    :return:
    """
    msg = result_msg
    if not msg:
        msg = RESULT_CODES.get(result_code, "")

    result = {"code": result_code, "msg": msg}
    if result_data is not None:
        result["data"] = result_data
    return jsonify(**result)


def gen_arguments():
    """
    取得请求参数
    :return:
    """
    req_json = request.json
    req_data = request.date
    req_form = request.form
    print req_json, req_data, req_form
    if req_json:
        return req_json
    if req_data:
        return req_data
    if req_form:
        return req_form
