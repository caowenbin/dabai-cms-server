# coding: utf-8
import datetime

from extends import db

__author__ = 'bin wen'


class ProductDao(object):
    @staticmethod
    def save(**values):
        """
        保存信息
        :param values:
        :return:
        """
        if "created_time" not in values:
            values["created_time"] = datetime.datetime.now()

        _id = db.master.insert(tablename="products", **values)
        return _id

    @staticmethod
    def save_pictures(product_id, insert_values, update_values, delete_values):
        """
        保存产品图片
        :param delete_values:
        :param product_id:
        :param insert_values:
        :param update_values:
        :return:
        """
        with db.master.transaction():
            _ids, update_count = 0, 0
            if insert_values:
                _ids = db.master.multiple_insert(tablename="product_pictures", values=insert_values)
            for v in update_values:
                _id = v.pop("id")
                update_count = db.master.update(tables="product_pictures", where={'id': _id}, **v)
            if delete_values:
                db.master.delete("product_pictures", vars={'ids': delete_values}, where=u"id in $ids")
            return _ids, update_count

    @staticmethod
    def save_goods(product_id, insert_values, update_values):
        """
        保存商品
        :param product_id:
        :param insert_values:
        :param update_values:
        :return:
        """
        with db.master.transaction():
            db.master.update(tables="goods", where={'product_id': product_id}, is_del=1)
            _ids, update_count = 0, 0
            if insert_values:
                _ids = db.master.multiple_insert(tablename="goods", values=insert_values)
            for v in update_values:
                if "is_del" not in v:
                    v["is_del"] = 0
                _id = v.pop("id")
                update_count = db.master.update(tables="goods", where={'id': _id}, **v)
            return _ids, update_count

    @staticmethod
    def get_detail(whats="*", _id=None, spu=None):
        """
        详情根据ID或编码查
        :param whats:
        :param _id:
        :param spu:
        :return:
        """
        where = {}
        if _id is not None:
            where["id"] = _id
        if spu is not None:
            where["spu"] = spu

        result = db.slave.select(tables=u"products", where=where, what=whats).first()

        return result

    @staticmethod
    def __gen_wheres_values(**kwargs):
        """
        生成查询条件及值
        :param kwargs:
        :rtype tuple:
        :return:
        """
        _ids = kwargs.get("_ids", [])
        first_category_id = kwargs.get("first_category_id", 0)
        second_category_id = kwargs.get("second_category_id", 0)
        third_category_id = kwargs.get("third_category_id", 0)
        short_name = kwargs.get("name", "")
        spu = kwargs.get("spu", "")
        query_type = kwargs.get("query_type", 0)
        supplier_id = kwargs.get("supplier_id")

        wheres = [u"p.is_del=0"]
        values = dict()

        if _ids:
            wheres.append(u"p.id in $_ids")
            values["_ids"] = _ids

        if query_type != -1:  # 有效的
            wheres.append(u"p.validity=$validity")
            values["validity"] = query_type

        if spu:
            wheres.append(u"spu like $spu")
            values["spu"] = u"%{}%".format(spu)

        if short_name:
            wheres.append(u"p.short_name like $short_name")
            values["short_name"] = u"%{}%".format(short_name)

        if first_category_id:
            wheres.append(u"first_category=$first_category_id")
            values["first_category_id"] = first_category_id
        if second_category_id:
            wheres.append(u"second_category=$second_category_id")
            values["second_category_id"] = second_category_id
        if third_category_id:
            wheres.append(u"third_category=$third_category_id")
            values["third_category_id"] = third_category_id

        if supplier_id:
            wheres.append(u"supplier_id=$supplier_id")
            values["supplier_id"] = supplier_id

        where_str = u" and ".join(wheres) if wheres else None

        return where_str, values if values else None

    @staticmethod
    def query_list(whats=None, is_show_picture=False, limit=None, offset=None, **kwargs):
        """
        分页查询信息
        :param whats:
        :param is_show_picture: 是否显示图片
        :param kwargs:
        :param limit:
        :param offset:
        :return:
        """
        where_str, values = ProductDao.__gen_wheres_values(**kwargs)

        if not whats:
            whats = (u"p.id, p.updated_time, third_category, title,spu,p.short_name,sales_volume,"
                     u"p.validity as validity, pi.image as images, p.full_name, "
                     u"s.short_name as supplier_name")

        if is_show_picture:
            tables = [(u"products as p left join product_pictures as pi "
                       u"on p.id = pi.product_id and pi.label = 0"),
                      u"suppliers as s"
                      ]
            where_str += u" and p.supplier_id = s.id"
        else:
            tables = u"products as p"
        data = db.slave.select(
            tables=tables,
            what=whats,
            vars=values,
            where=where_str,
            limit=limit,
            offset=offset,
            order=u"p.updated_time DESC"
        )

        return data

    @staticmethod
    def get_total_count(**kwargs):
        """
        获取对应的条数
        :param kwargs:
        :return:
        """
        where_str, values = ProductDao.__gen_wheres_values(**kwargs)
        counts = db.slave.select(
            tables=u"products as p",
            what=u"count(id) as counts",
            vars=values,
            where=where_str
        ).first().counts

        return counts

    @staticmethod
    def update(_id, **update_value):
        """
        修改
        :param _id:
        :param update_value:
        :return:
        """

        with db.master.transaction():
            update_count = db.master.update(
                    tables="products",
                    vars={'id': _id},
                    where="id=$id ",
                    **update_value
            )

            return update_count
        return 0

    @staticmethod
    def query_goods_list(product_id=None, whats="*", filter_del=None):
        """
        根据货品ID获取商品列表
        :param product_id:
        :param whats:
        :param filter_del: 0正常 1删除
        :return:
        """
        wheres = {"is_del": 0}
        if product_id:
            wheres.update({"product_id": product_id})
        if filter_del is not None:
            wheres["is_del"] = filter_del
        data = db.slave.select(
            tables=u"goods",
            what=whats,
            where=wheres,
            order=u"id"
        )

        return data

    @staticmethod
    def query_pictures_list(product_id, whats="*", label=None):
        """
        根据货品ID获取图片列表
        :param product_id:
        :param whats:
        :param label: 图片标记 0封面 1橱窗
        :return:
        """
        wheres = {"product_id": product_id}
        if label is not None:
            wheres["label"] = label

        data = db.slave.select(
            tables=u"product_pictures",
            what=whats,
            where=wheres,
            order=u"ordering"
        )

        return data

    @staticmethod
    def set_validity(ids, validity):
        """
        上架或下架
        :param ids: list类型
        :param validity:
        :return:
        """
        set_values = dict(validity=validity)

        result = db.master.update('products', vars={'ids': ids}, where="id in $ids ", **set_values)

        return result

    @staticmethod
    def delete(ids):
        """
        删除
        :param ids:
        :return:
        """
        set_values = dict(is_del=1)
        result = db.master.update("products", vars={'ids': ids}, where=u"id in $ids", **set_values)
        return result

products = ProductDao
