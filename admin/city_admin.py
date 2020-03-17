# coding: utf-8
import datetime
import logging

from flask import request
from flask.ext.admin import expose

from cores.adminweb import BaseHandler
from dao.citydao import cities
from libs.flask_login import login_required

__author__ = 'bin wen'

_log = logging.getLogger("ADMIN")
_handler_log = logging.getLogger("HANDLER")


class CityHandler(BaseHandler):
    """
    可送达城市列表
    """
    @expose('/')
    @expose('/city/list.html')
    @login_required
    def list_view(self):
        city_list = cities.query_list(whats=u"province_code, city_code, area_code")
        results = set()
        for info in city_list:
            for k in info:
                results.add(str(info[k]))

        return self.render(template="city/list.html", data=list(results))

    @expose('/city/create.html', methods=('POST',))
    @login_required
    def create_view(self):
        city_data = request.form.get("cities", "")
        full_area_list = city_data.split(";")
        insert_values = []
        for area in full_area_list:
            if not area:
                continue
            province_city_area = area.split("#")
            insert_values.append(
                {"province_code": province_city_area[0],
                 "province_name": province_city_area[1],
                 "city_code": province_city_area[2],
                 "city_name": province_city_area[3],
                 "area_code": province_city_area[4],
                 "area_name": province_city_area[5],
                 "created_time": datetime.datetime.now()
                 }
            )
        result = cities.save(*insert_values)

        return self.make_write(result_code=0, result_data=self.reverse_url(".list_view"))