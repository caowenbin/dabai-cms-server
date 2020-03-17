#!/usr/bin/env python
# coding: utf8

import codecs
import json

from requests import request

params = {}
params.update({
    'key': 'BT7BZ-6MRCO-6TDW3-SRWMR-JWQ6Q-ACFQV',
    'output': 'json'
})

kwargs = {'params': params}
response = request("GET", "http://apis.map.qq.com/ws/district/v1/list", **kwargs)
result = response.json().get("result")
print json.dumps(result)
province_list = result[0]
city_list = result[1]
district_list = result[2]
province_dict = {}
# fd = codecs.open("ChinaCity.js", "w+", "utf-8")
all_city_list = []
# province_dict_str = u"var province={"
# city_str = u""
# district_str = u""
for province in province_list:
    # province_dict_str += u"'{}': {}, ".format(province["fullname"], province["id"])
    # province_dict[province["fullname"]] = province["id"]
    province_id = province["id"]
    p_name = province["fullname"]
    data_str = u""
    if p_name == u"台湾":
        continue
    if p_name in (u"北京市", u"天津市", u"上海市", u"重庆市"):
        _province_id = province_id + "00"
        data_str += _province_id + "#" + p_name[:-1] +"#" +province_id + "#" + p_name+"#"
        all_city_list.append({"id": _province_id, "pId": "0", "name": u"(直辖市)"+p_name[:-1]})
        all_city_list.append({"id": province_id, "pId": _province_id, "name": p_name})
    else:
        all_city_list.append({"id": province_id, "pId": "0", "name": p_name})
        data_str += province_id + "#" + p_name+"#"

    if province.get("cidx", []):
        left, right = province.get("cidx")
        children = city_list[left:right + 1]
        # city_str += u", {}: ".format(province["id"]) + u"{"
        for child in children:
            # city_str += u"'{}': {}, ".format(child["fullname"], child["id"])
            city_id = child["id"]
            # data_str += city_id + "#" + child["fullname"]

            if child.get("cidx", []):
                all_city_list.append({"id": city_id, "pId": province_id, "name": child["fullname"]})
                left, right = child.get("cidx")
                districts = district_list[left:right + 1]
                # district_str += u", {}: ".format(child["id"]) + u"{"
                if districts:
                    for district in districts:
                        all_city_list.append({"id": district["id"], "pId": city_id,
                                              "name": district["fullname"],
                                              "data": data_str +city_id + "#" + child["fullname"]+ "#" + district["id"] +"#"+district["fullname"]
                                              })
            elif p_name not in (u"北京市", u"天津市", u"上海市", u"重庆市"):
                all_city_list.append({"id": city_id, "pId": province_id, "name": child["fullname"]})
                all_city_list.append({"id": city_id+"00",
                                      "pId": city_id,
                                      "name": u"本全区域",
                                      "data": data_str +city_id + "#" + child["fullname"]+ "#" + city_id+"00" + u"#本全区域"
                                      })
            else:
                all_city_list.append({"id": city_id, "pId": province_id,
                                      "name": child["fullname"],
                                      "data": data_str+city_id + "#" + child["fullname"]
                                      })

                        # district_str += u"'{}': {}, ".format(district["fullname"], district["id"])
                # district_str = district_str.rstrip(", ") + u"}"
        # city_str = city_str.rstrip(", ") + u"}"
# province_dict_str = province_dict_str.rstrip(", ") + "}"
# city_str = u"var city={" + city_str.lstrip(", ")
# city_str = city_str.rstrip(", ") + u"}"
# district_str = u"var district={" + district_str.lstrip(", ")
# district_str = district_str.rstrip(", ") + u"}"

# fd.write(province_dict_str)
# fd.write(";\n")
# fd.write(city_str)
# fd.write(";\n")
# fd.write(district_str)
# fd.close()
print json.dumps(all_city_list)