# coding: utf-8
import datetime
from itertools import islice

from extends import db
from utils.dateutils import datetime2str

__author__ = 'bin wen'


class CategoryDao(object):
    @staticmethod
    def save(name, parent_id):
        """
        保存分类信息
        :param name:
        :param parent_id:
        :return:
        """
        result = db.master.insert(
                tablename="categories",
                name=name,
                created_time=datetime.datetime.now(),
                parent_id=parent_id
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
        parent_id = kwargs.get("parent_id")
        name = kwargs.get("name", "")
        query_type = kwargs.get("query_type", -1)

        wheres = []
        values = {}

        if parent_id is not None:
            wheres.append(u"parent_id=$parent_id")
            values["parent_id"] = parent_id

        if query_type != -1:  # 有效的
            wheres.append(u"validity=$validity")
            values["validity"] = query_type

        if name:
            wheres.append(u"name like $name")
            values["name"] = u"%{}%".format(name)

        where_str = u" and ".join(wheres) if wheres else None

        return where_str, values if values else None

    @staticmethod
    def query_list(query_type=-1, whats=None, name=None, parent_id=None, limit=None, offset=None):
        """
        分页查询信息
        :param query_type: -1全部 1有效 0注销
        :param whats:
        :param name:
        :param parent_id:
        :param limit:
        :param offset:
        :return:
        """
        where_str, values = CategoryDao.__gen_wheres_values(
            name=name,
            parent_id=parent_id,
            query_type=query_type
        )
        if not whats:
            whats = u"id, name, created_time, updated_time, validity"
        results = db.slave.select(
            tables=u"categories",
            what=whats,
            vars=values,
            where=where_str,
            limit=limit,
            offset=offset,
            order=u"updated_time DESC"
        )

        return results

    @staticmethod
    def query_child_category(name=None, parent_id=0, limit=None, offset=None):
        """
        查询子类信息
        :param name:
        :param parent_id:
        :param limit:
        :param offset:
        :return:
        """
        where_str, values = CategoryDao.__gen_wheres_values(
            parent_id=parent_id,
            name=name,
            query_type=1
        )

        data = db.slave.select(
            tables=u'categories',
            what=u"id,name,created_time",
            vars=values,
            where=where_str,
            limit=limit,
            offset=offset,
            order=u"created_time DESC"
        )

        results = [{"id": r.id, "name": r.name, "created_time": datetime2str(r.created_time)} for r in data]

        return results

    @staticmethod
    def get_total_count(query_type=-1, name=None, parent_id=0):
        """
        获取对应的条数
        :param query_type: -1全部 1有效 0注销
        :param name:
        :param parent_id:
        :return:
        """
        where_str, values = CategoryDao.__gen_wheres_values(
            query_type=query_type,
            name=name,
            parent_id=parent_id
        )

        counts = db.slave.select(
            tables='categories',
            what="count(id) as counts",
            vars=values,
            where=where_str
        ).first().counts

        return counts

    @staticmethod
    def get_detail(_id, whats="*"):
        """
        详情
        :param _id:
        :param whats:
        :return:
        """
        result = db.slave.select(tables=u"categories", what=whats, where={'id': _id}).first()
        return result

    @staticmethod
    def get_category_by_id(*ids):
        """
        根据多个ID获取对应的记录名称
        :param ids:
        :return:
        """
        result = db.slave.select(
                tables=u"categories",
                where=u"id in $ids",
                what=u"id, name",
                vars={'ids': list(ids)}
        )
        category_dict = {r.id: r.name for r in result}
        return category_dict

    @staticmethod
    def gen_full_category(category_id):
        """
        根据第三级分类ID获取完整分类
        :param category_id:
        :return:
        """
        def __get_category(c_id):
            while True:
                category_info = category.get_detail(_id=c_id)
                yield category_info.id, category_info.name
                c_id = category_info.parent_id

        category_list = tuple(islice(__get_category(category_id), 3))

        return category_list

    @staticmethod
    def set_validity(ids, validity):
        """
        批量注销或激活
        :param ids:
        :param validity:
        :return:
        """
        set_values = dict(validity=validity)

        result = db.master.update('categories', vars={'ids': ids}, where="id in $ids ", **set_values)

        return result

    @staticmethod
    def update(_id, name):
        """
        修改
        :param _id:
        :param name:
        :return:
        """
        result = db.master.update('categories', vars={'id': _id}, where="id=$id ", name=name)

        return result

category = CategoryDao
