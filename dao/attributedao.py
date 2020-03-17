# coding: utf-8
import datetime

from extends import db
from dao.categorydao import category

__author__ = 'bin wen'


class AttributeDao(object):
    @staticmethod
    def save(category_id, name, attribute_item):
        """
        保存属性信息
        :param category_id:
        :param name:
        :param attribute_item:
        :return:
        """
        with db.master.transaction():
            attribute_id = db.master.insert(
                tablename="attributes",
                name=name,
                created_time=datetime.datetime.now(),
                category_id=category_id
            )

            values = [dict(attr_id=attribute_id,
                           created_time=datetime.datetime.now(),
                           attr_value=item,
                           ordering=index) for index, item in enumerate(attribute_item, 1)]

            item_ids = db.master.multiple_insert(tablename="attribute_items", values=values)

        return attribute_id

    @staticmethod
    def __gen_wheres_values(**kwargs):
        """
        生成查询条件及值
        :param kwargs:
        :rtype tuple:
        :return:
        """
        category_id = kwargs.get("category_id", 0)
        name = kwargs.get("name", "")

        wheres = [u"is_del=0"]
        values = dict()

        if name:
            wheres.append(u"name like $name")
            values["name"] = u"%{}%".format(name)
        if category_id:
            wheres.append(u"category_id=$category_id")
            values["category_id"] = category_id

        where_str = u" and ".join(wheres) if wheres else None

        return where_str, values if values else None

    @staticmethod
    def query_list(name=None, category_id=None, limit=None, offset=None):
        """
        分页查询信息
        :param name:
        :param category_id:
        :param limit:
        :param offset:
        :return:
        """
        where_str, values = AttributeDao.__gen_wheres_values(
            category_id=category_id,
            name=name
        )

        data = db.slave.select(
            tables=u"attributes",
            what=u"id, updated_time, category_id, name, ordering",
            vars=values,
            where=where_str,
            limit=limit,
            offset=offset,
            order=u"updated_time DESC"
        )

        results = []
        attr_ids = []

        for r in data:
            attr_ids.append(r.id)
            r["category"] = category.gen_full_category(r.category_id)
            results.append(r)

        if attr_ids:
            attribute_items = AttributeDao.query_attribute_items(attr_ids=attr_ids)
            for r in results:
                _values_temp = attribute_items.get(r.id, [])
                item_values = [v[1] for v in _values_temp]
                r["item_values"] = item_values

        return results

    @staticmethod
    def query_attribute_items(attr_ids):
        """
        获得属性选项值
        :param attr_ids:
        :return:
        """
        data = db.slave.select(
            tables=u"attribute_items",
            what=u"id, attr_id, attr_value",
            vars={u'ids': attr_ids},
            where=u"attr_id in $ids and is_del=0",
            order=u"attr_id, ordering"
        )

        results = {}
        for item in data:
            attr_id = item.attr_id
            if attr_id in results:
                results[attr_id].append((item.id, item.attr_value))
            else:
                results.setdefault(attr_id, [(item.id, item.attr_value)])

        return results

    @staticmethod
    def get_total_count(name=None, category_id=None):
        """
        获取对应的条数
        :param name:
        :param category_id:
        :return:
        """
        where_str, values = AttributeDao.__gen_wheres_values(
            category_id=category_id,
            name=name
        )
        counts = db.slave.select(
            tables=u"attributes",
            what=u"count(id) as counts",
            vars=values,
            where=where_str
        ).first().counts

        return counts

    @staticmethod
    def get_detail(_id):
        """
        详情
        :param _id:
        :return:
        """
        result = db.slave.select(tables=u"attributes", where={'id': _id}).first()
        attribute_items = AttributeDao.query_attribute_items(attr_ids=[_id])
        result["item_values"] = attribute_items.get(result.id, [])

        return result

    @staticmethod
    def update(_id, name=None, attribute_items=None):
        """
        修改
        attribute_items = [(tag, id, name)]
        tag 0插入 1修改 2删除

        :param _id:
        :param name:
        :param attribute_items:
        :return:
        """
        with db.master.transaction():
            update_count = db.master.update(
                tables="attributes",
                vars={'id': _id}, where="id=$id ",
                name=name
            )

            insert_values = []
            del_values = []
            for index, item in enumerate(attribute_items, 1):
                tag = item[0]
                if tag == 0:
                    insert_values.append(
                        dict(attr_id=_id,
                             created_time=datetime.datetime.now(),
                             attr_value=item[2],
                             ordering=index
                             )
                    )
                    continue
                if tag == 2:
                    del_values.append(item[1])
                    continue

                db.master.update(
                    tables="attribute_items",
                    vars={'id': item[1]}, where="id=$id ",
                    attr_value=item[2], ordering=index
                )

            if insert_values:
                db.master.multiple_insert(tablename="attribute_items", values=insert_values)

            if del_values:
                db.master.update(
                    tables="attribute_items",
                    vars={'id': del_values}, where="id in $id ",
                    is_del=1
                )

        return update_count

    @staticmethod
    def get_active_attribute(category_id):
        """
        根据分类获取有效的产品属性与选项值
        :param category_id:
        :return:
        """
        where_str, values = AttributeDao.__gen_wheres_values(category_id=category_id)

        data = db.slave.select(
            tables=u"attributes",
            what=u"id, name",
            vars=values,
            where=where_str,
            order=u"ordering asc"
        )

        results = []
        attr_ids = []

        for r in data:
            attr_ids.append(r.id)
            results.append(r)

        if attr_ids:
            attribute_items = AttributeDao.query_attribute_items(attr_ids=attr_ids)
            for r in results:
                _values_temp = attribute_items.get(r.id, [])
                r["item_values"] = _values_temp

        return results

    @staticmethod
    def delete(ids):
        """
        批量注销或激活
        :param ids:
        :return:
        """
        set_values = dict(is_del=1)

        result = db.master.update('attributes', vars={'ids': ids}, where="id in $ids ", **set_values)

        return result


attribute = AttributeDao
