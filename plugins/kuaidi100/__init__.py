#!/usr/bin/env python
# coding: utf8
__author__ = 'ye shuo'

import os
import xlrd


def analyse_xlsx():
    data = xlrd.open_workbook(os.getcwd().replace("\\", "/") + "/plugins/kuaidi100/kuaidi.xlsx")
    table = data.sheets()[0]
    rows = table.nrows
    data_list = []
    for i in range(1, rows):
        row_value = table.row_values(i)
        data_list.append({
            "name": row_value[0],
            "code": row_value[1],
            "type": row_value[-1]
        })

    return data_list
