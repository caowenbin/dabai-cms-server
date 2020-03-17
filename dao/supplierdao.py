# coding: utf-8
import datetime

from extends import db
__author__ = 'bin wen'


class SupplierDao(object):
    """
    供应商DAO
    """

    @staticmethod
    def __gen_wheres_values(**kwargs):
        """
        生成查询条件及值
        :param kwargs:
        :rtype tuple:
        :return:
        """
        wheres = []
        values = dict()
        query_type = kwargs.get("query_type", -1)
        login_name = kwargs.get("login_name", "")
        fullname = kwargs.get("fullname", "")
        contact_name = kwargs.get("contact_name", "")
        contact_phone = kwargs.get("contact_phone", "")
        if query_type != -1:  # 有效的
            wheres.append(u"validity=$validity")
            values["validity"] = query_type

        if fullname:
            wheres.append(u"fullname like $fullname")
            values["fullname"] = u"%{}%".format(fullname)

        if login_name:
            wheres.append(u"login_name like $login_name")
            values["login_name"] = u"%{}%".format(login_name)

        if contact_name:
            wheres.append(u"contact_name like $contact_name")
            values["contact_name"] = u"%{}%".format(contact_name)

        if contact_phone:
            wheres.append(u"contact_phone=$contact_phone")
            values["contact_phone"] = contact_name

        where_str = u" and ".join(wheres) if wheres else None

        return where_str, values

    @staticmethod
    def query_list(whats=None, query_type=-1, fullname=None, login_name=None, contact_name=None,
                   contact_phone=None, limit=None, offset=None):
        """
        分页查询信息
        :param whats: 返回的字段
        :param query_type:
        :param fullname:
        :param login_name:
        :param contact_name:
        :param contact_phone:
        :param limit:
        :param offset:
        :return:
        """
        where_str, values = SupplierDao.__gen_wheres_values(
            query_type=query_type,
            fullname=fullname,
            login_name=login_name,
            contact_name=contact_name,
            contact_phone=contact_phone
        )

        if not whats:
            whats = (u"id, short_name, updated_time, fullname, login_name, contact_name, "
                     u"contact_phone, validity, last_login_time, last_login_ip")
        results = db.slave.select(
            tables=u"suppliers",
            what=whats,
            vars=values,
            where=where_str,
            limit=limit,
            offset=offset,
            order=u"updated_time DESC"
        )

        return results

    @staticmethod
    def get_total_count(query_type=-1, fullname=None, login_name=None, contact_name=None, contact_phone=None):
        """
        获取对应的条数
        :param query_type:
        :param fullname:
        :param login_name:
        :param contact_name:
        :param contact_phone:
        :return:
        """
        where_str, values = SupplierDao.__gen_wheres_values(
            query_type=query_type,
            fullname=fullname,
            login_name=login_name,
            contact_name=contact_name,
            contact_phone=contact_phone
        )

        counts = db.slave.select(
            tables='suppliers',
            what="count(id) as counts",
            vars=values,
            where=where_str
        ).first().counts

        return counts

    @staticmethod
    def __gen_set_value(**kwargs):
        """
        生成操作的数据值
        :param kwargs:
        :return:
        """
        set_values = {}
        password = kwargs.get("password")
        fullname = kwargs.get("fullname")
        contact_name = kwargs.get("contact_name")
        contact_phone = kwargs.get("contact_phone")
        remote_ip = kwargs.get("remote_ip")
        operator = kwargs.get("operator")
        short_name = kwargs.get("short_name")
        login_name = kwargs.get("login_name")

        if fullname is not None:
            set_values["fullname"] = fullname
        if contact_name is not None:
            set_values["contact_name"] = contact_name
        if password is not None:
            set_values["password"] = password
        if contact_phone is not None:
            set_values["contact_phone"] = contact_phone
        if remote_ip is not None:
            set_values["last_login_ip"] = remote_ip
            set_values["last_login_time"] = datetime.datetime.now()

        if operator is not None:
            set_values["operator"] = operator

        if short_name is not None:
            set_values["short_name"] = short_name

        if login_name is not None:
            set_values["login_name"] = login_name

        return set_values

    @staticmethod
    def save(**kwargs):
        _set_values = SupplierDao.__gen_set_value(**kwargs)
        if "validity" not in _set_values:
            _set_values["validity"] = 1

        if "created_time" not in _set_values:
            _set_values["created_time"] = datetime.datetime.now()

        result = db.master.insert(tablename="suppliers", **_set_values)
        return result

    @staticmethod
    def update(_id, **kwargs):
        """
        修改
        :param _id:
        :param kwargs:
        :return:
        """
        _set_values = SupplierDao.__gen_set_value(**kwargs)
        result = db.master.update('suppliers', vars={'id': _id}, where="id=$id ", **_set_values)

        return result

    @staticmethod
    def set_validity(ids, validity):
        """
        注销或激活
        :param ids: list类型
        :param validity:
        :return:
        """
        set_values = dict(validity=validity)

        result = db.master.update('suppliers', vars={'ids': ids}, where="id in $ids ", **set_values)

        return result

    @staticmethod
    def get_detail(whats="*", _id=None, login_name=None):
        """
        详情
        :param whats:
        :param _id:
        :param login_name:
        :return:
        """
        where = {}
        if _id is not None:
            where["id"] = _id
        if login_name is not None:
            where["login_name"] = login_name

        result = db.slave.select(tables=u"suppliers", where=where, what=whats).first()

        return result

suppliers = SupplierDao
