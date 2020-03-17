# coding: utf-8
import datetime

from extends import db

__author__ = 'bin wen'


class AdminUserDao(object):

    @staticmethod
    def save(email, password, fullname, is_admin):
        """
        保存用户信息
        :param email:
        :param password:
        :param fullname:
        :param is_admin:
        :return:
        """
        result = db.master.insert(
                tablename="administrators",
                email=email,
                created_time=datetime.datetime.now(),
                password=password,
                fullname=fullname,
                administer=is_admin,
                validity=1,
                confirmed=1
        )

        return result

    @staticmethod
    def __gen_wheres_values(**kwargs):
        """
        生成查询条件及值
        :param kwargs:
        :rtype tuple:
        :return:
        """
        wheres = [u"confirmed=1"]
        values = dict()
        query_type = kwargs.get("query_type", -1)
        email = kwargs.get("email", "")
        fullname = kwargs.get("fullname", "")
        if query_type != -1:  # 有效的
            wheres.append(u"validity=$validity")
            values["validity"] = query_type

        if email:
            wheres.append(u"email like $email")
            values["email"] = u"%{}%".format(email)

        if fullname:
            wheres.append(u"fullname like $fullname")
            values["fullname"] = u"%{}%".format(fullname)

        where_str = u" and ".join(wheres) if wheres else None

        return where_str, values

    @staticmethod
    def query_list(query_type=-1, email=None, fullname=None, limit=10, offset=0):
        """
        分页查询信息
        :param query_type: -1全部 1有效 0注销
        :param email:
        :param fullname:
        :param limit:
        :param offset:
        :return:
        """
        where_str, values = AdminUserDao.__gen_wheres_values(
            query_type=query_type,
            email=email,
            fullname=fullname
        )

        results = db.slave.select(
            tables=u'administrators',
            what=u"id,email,fullname,administer,validity,updated_time,last_login_time,last_login_ip",
            vars=values,
            where=where_str,
            limit=limit,
            offset=offset,
            order=u"updated_time DESC"
        )

        return results

    @staticmethod
    def get_total_count(query_type=-1, email=None, fullname=None):
        """
        获取对应的条数
        :param query_type:
        :param email:
        :param fullname:
        :return:
        """
        where_str, values = AdminUserDao.__gen_wheres_values(
            query_type=query_type,
            email=email,
            fullname=fullname
        )

        counts = db.slave.select(
            tables='administrators',
            what="count(id) as counts",
            vars=values,
            where=where_str
        ).first().counts

        return counts

    @staticmethod
    def get_detail(whats="*", _id=None, login_name=None, confirmed=None):
        """
        详情
        :param whats:
        :param _id:
        :param login_name:
        :param confirmed:
        :return:
        """
        where = {}
        if _id is not None:
            where["id"] = _id
        if login_name is not None:
            where["email"] = login_name
        if confirmed is not None:
            where["confirmed"] = confirmed

        result = db.slave.select(tables=u"administrators", what=whats, where=where).first()
        return result

    @staticmethod
    def update(_id, password=None, fullname=None, is_admin=None, remote_ip=None):
        """
        修改
        :param _id:
        :param password:
        :param fullname:
        :param is_admin:
        :param remote_ip: 登录IP
        :return:
        """
        set_values = {}
        if fullname is not None:
            set_values["fullname"] = fullname
        if is_admin is not None:
            set_values["administer"] = is_admin
        if password is not None:
            set_values["password"] = password
        if remote_ip is not None:
            set_values["last_login_ip"] = remote_ip
            set_values["last_login_time"] = datetime.datetime.now()

        result = db.master.update('administrators', vars={'id': _id}, where="id=$id ", **set_values)

        return result

    @staticmethod
    def delete(*_id):
        """
        批量删除
        :param _id:
        :return:
        """
        result = db.master.delete('administrators', vars={'ids': list(_id)}, where="id in $ids")

        return result

    @staticmethod
    def set_validity(ids, validity):
        """
        批量注销或激活
        :param ids:
        :param validity:
        :return:
        """
        set_values = dict(validity=validity)
        result = db.master.update('administrators', vars={'ids': ids}, where="id in $ids ", **set_values)

        return result

admin = AdminUserDao
