# coding: utf-8
import logging
import os
import random
import datetime

from flask import request, current_app
from flask.ext.admin import expose

from cores.actions import action
from cores.adminweb import BaseHandler
from dao.categorydao import category
from dao.productdao import products
from dao.supplierdao import suppliers
from extends import csrf
from libs.flask_login import login_required
from utils.function_data_flow import flow_tools
from utils.utils import utf8

__author__ = 'bin wen'

_log = logging.getLogger("ADMIN")
_handler_log = logging.getLogger("HANDLER")


class ProductHandler(BaseHandler):
    """
    商品列表
    """

    column_list = ("images", "spu", "product_name", "sales_volume", "supplier_name",
                   "validity", "updated_time")

    column_labels = {
        "spu": u"货品编码",
        "product_name": u"货品名称",
        "sales_volume": u"销量",
        "updated_time": u"变更时间",
        "images": u"产品封面",
        "supplier_name": u"供应商",
        "validity": u"状态",
    }
    column_widget_args = {
        "sales_volume": {'class': "hidden-480"},
        "updated_time": {'class': "hidden-480"},
        "validity": {'class': "hidden-480"}
    }
    tabs_list = (
        {"query_type": -1, "name": u"全部"},
        {"query_type": 1, "name": u"可售卖的"},
        {"query_type": 2, "name": u"待完善的"},
        {"query_type": 0, "name": u"已下架"}
    )

    @expose('/')
    @expose('/product/list.html')
    @login_required
    def list_view(self):
        page = request.args.get('page', 0, type=int)
        name = request.args.get("name", "")
        spu = request.args.get("spu", "")
        first_category_id = request.args.get("first_category_id", "")
        second_category_id = request.args.get("second_category_id", "")
        third_category_id = request.args.get("third_category_id", "")
        query_type = request.args.get("query_type", 1, type=int)
        supplier_id = request.args.get("supplier_id", 0)
        query_kwargs = dict(
            name=name,
            first_category_id=first_category_id,
            second_category_id=second_category_id,
            third_category_id=third_category_id,
            spu=spu,
            query_type=query_type,
            supplier_id=supplier_id
        )

        def pager_url(p):
            if p is None:
                p = 0

            return self._get_url('.list_view', p, **query_kwargs)

        count = products.get_total_count(**query_kwargs)

        results = []
        num_pages = 0

        if count > 0:
            num_pages = self.gen_total_pages(count)
            if num_pages - 1 < page:
                page -= 1

            offset_value = page * self.page_size
            results = products.query_list(
                is_show_picture=True,
                limit=self.page_size,
                offset=offset_value,
                **query_kwargs
            )

        actions, actions_confirmation = self.get_actions_list()
        return_url = self.gen_return_url(".list_view", page=page, **query_kwargs)
        _supplier_list = flow_tools.gen_suppliers(query_type=-1)

        return self.render(
            template="product/list.html",
            actions=actions,
            actions_confirmation=actions_confirmation,
            count=count,
            page=page,
            num_pages=num_pages,
            pager_url=pager_url,
            data=results,
            query_kwargs=query_kwargs,
            return_url=return_url,
            column_list=self.column_list,
            column_labels=self.column_labels,
            column_widget_args=self.column_widget_args,
            tabs_list=self.tabs_list,
            suppliers=_supplier_list
        )

    @expose('/product/action.html', methods=('POST',))
    @login_required
    def action_view(self):
        return_url = request.form.get("return_url", "")
        return self.handle_action(return_view=return_url)

    @action('disable', u"注销(下架)所选", u"你确定要注销(下架)所选的记录?")
    def action_disable(self, ids):
        try:
            result = products.set_validity(ids, validity=0)
            _handler_log.info(u"[AdminListHandler] batch disable, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[AdminListHandler] batch disable error")

    @action('activate', u"激活(上架)选择", u"你确定要激活所选的记录?")
    def action_activate(self, ids):
        try:
            result = products.set_validity(ids, validity=1)
            _handler_log.info(u"[AdminListHandler] batch activate, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[AdminListHandler] batch activate error.")

    @action('delete', u"删除所选", u"你确定要删除所选的记录?")
    def action_delete(self, ids):
        try:
            result = products.delete(ids)
            _handler_log.info(u"[AdminListHandler] batch delete, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[AdminListHandler] batch delete error")

    @expose('/product/create.html', methods=('GET', 'POST'))
    @login_required
    def create_view(self):
        """
        基本信息
        :return:
        """
        if request.method == "GET":
            result = {
                "id": 0,
                "brands": flow_tools.gen_brands(),
                "suppliers": flow_tools.gen_suppliers(query_type=-1)
            }

            return self.render(template=u"product/create_basic.html", data=result)
        else:
            req_data = self.gen_arguments
            spu = req_data.get("spu")
            detail = products.get_detail(whats="id", spu=spu)
            if detail:
                return self.make_write(result_code=4000)

            first_category = int(req_data.get("first_category"))
            second_category = int(req_data.get("second_category"))
            third_category = int(req_data.get("third_category"))
            attributes = flow_tools.gen_product_properties(third_category)  # 校验分类是否添加属性
            if not attributes:
                return self.make_write(result_code=2003)

            product_type = int(req_data.get("product_type"))
            full_name = req_data.get("full_name")
            title = req_data.get("title")
            short_name = req_data.get("short_name")
            brand_name = req_data.get("brand_name")
            supplier_id = int(req_data.get("supplier_id"))
            sales_volume = int(req_data.get("sales_volume", 0))
            limits = int(req_data.get("limits", 0))
            market_text = req_data.get("market_text")
            about_text = req_data.get("about_text")
            out_way = int(req_data.get("out_way"))
            save_values = dict(
                first_category=first_category,
                second_category=second_category,
                third_category=third_category,
                product_type=product_type,
                spu=spu,
                full_name=full_name,
                title=title,
                short_name=short_name,
                brand_name=brand_name,
                supplier_id=supplier_id,
                sales_volume=sales_volume,
                limits=limits,
                market_text=market_text,
                about_text=about_text,
                out_way=out_way,
                image_text="",
                validity=1
            )
            _id = products.save(**save_values)
            redirect_url = u"{url}?id={id}&ed={is_edit}&category_id={category_id}".format(
                    url=self.reverse_url(".product_attributes_view"),
                    id=_id,
                    is_edit=0,
                    category_id=third_category
            )
            return self.make_write(result_code=0, result_data=redirect_url)

    @expose('/product/edit.html', methods=('GET', 'POST'))
    @login_required
    def edit_view(self):
        if request.method == "GET":
            p_id = request.args.get("id", 0, type=int)
            query_kwargs = {
                "id": p_id,
                "is_edit": 1,
                "brands": flow_tools.gen_brands(),
                "suppliers": flow_tools.gen_suppliers(query_type=-1)
            }

            result = products.get_detail(_id=p_id)
            category_list = category.gen_full_category(result.third_category)
            result["category_list"] = category_list
            supplier_detail = suppliers.get_detail(whats="fullname", _id=result.supplier_id)
            result["supplier_name"] = supplier_detail.fullname

            return self.render(
                    template=u"product/edit_basic.html",
                    data=result,
                    query_kwargs=query_kwargs
            )

        else:
            req_data = self.gen_arguments
            _id = int(req_data.get("id"))
            full_name = req_data.get("full_name")
            title = req_data.get("title")
            short_name = req_data.get("short_name")
            sales_volume = int(req_data.get("sales_volume", 0))
            limits = int(req_data.get("limits", 0))
            market_text = req_data.get("market_text")
            about_text = req_data.get("about_text")
            out_way = int(req_data.get("out_way"))
            update_values = dict(
                    full_name=full_name,
                    title=title,
                    short_name=short_name,
                    sales_volume=sales_volume,
                    limits=limits,
                    market_text=market_text,
                    about_text=about_text,
                    out_way=out_way
            )
            result = products.update(_id=_id, **update_values)
            redirect_url = u"{url}?id={id}&ed={is_edit}&category_id={category_id}".format(
                    url=self.reverse_url(".product_attributes_view"),
                    id=_id,
                    is_edit=1,
                    category_id=req_data("category_id", 0)
            )
            return self.make_write(result_code=0, result_data=redirect_url)

    @staticmethod
    def gen_sku(prefix, attr_id):
        """
        1+供应商编码+三类+货品编码+属性+ 随机数
        :param prefix:
        :param attr_id:
        :return:
        """
        sku = u"{prefix}{attr_id:0>3}{v}".format(
                prefix=prefix,
                attr_id=attr_id,
                v=''.join(random.sample(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'), 3))
        )

        return sku

    @expose('/product/attributes.html', methods=('GET', 'POST'))
    @login_required
    def product_attributes_view(self):
        if request.method == "GET":
            p_id = request.args.get("id", 0, type=int)
            is_edit = request.args.get("ed")
            category_id = int(request.args.get("category_id", 0))
            query_kwargs = {
                "id": p_id,
                "is_edit": is_edit,
                "category_id": category_id,
                "attributes": flow_tools.gen_product_properties(category_id)
            }
            attr_items = set()
            product_properties = None
            if is_edit == "1":
                goods_list = products.query_goods_list(
                        whats=u"id, price, stock, is_default, properties",
                        product_id=p_id,
                        filter_del=0
                )
                _properties = {}
                for g in goods_list:
                    property_list = [p.split(":")[-1] for p in g.properties.split("^")]
                    property_list.sort()
                    attr_items.update(property_list)
                    key = "".join(property_list)
                    _properties[key] = {
                        "property_id": g.id,
                        "price": float(g.price) / 100.0,
                        "is_default": g.is_default,
                        "stock": g.stock
                    }
                product_properties = _properties

            result = {
                "product_attr_items": attr_items,
                "product_properties": product_properties
            }

            return self.render(
                    template=u"product/goods.html",
                    data=result,
                    query_kwargs=query_kwargs
            )

        else:
            req_data = self.gen_arguments
            _id = req_data.get("id")  # 货品ID
            # 属性ID与属性选项ID组合,即12:1216^16:1626^18:1864
            properties_list = req_data.getlist("properties")
            # 属性名与属性选项名组合,即性别:女^颜色:白^尺寸:X
            property_names_list = req_data.getlist("property_names")
            price_list = req_data.getlist("price")  # 商品价格
            stock_list = req_data.getlist("stock")  # 商品库存
            is_default_index = req_data.get("is_default")  # 默认作为货品第一款数据下标
            property_id_list = req_data.getlist("property_id")  # 商品ID

            product_detail = products.get_detail(whats="id, third_category, supplier_id", _id=_id)
            prefix = u"1{supplier_id:0>2}{category_id:0>2}{p_id:0>4}".format(
                    supplier_id=str(product_detail.supplier_id)[:2],
                    category_id=str(product_detail.third_category)[:2],
                    p_id=str(_id)[:4]
            )

            insert_values = []
            update_values = []
            for index, v in enumerate(zip(properties_list, property_names_list, price_list, stock_list, property_id_list)):
                attr_id = v[0].split("^")[-1].split(":")[-1]
                temp = {
                    "price": int(float(v[2]) * 100),
                    "stock": v[3],
                    "product_id": _id,
                    "property_names": v[1],
                    "properties": v[0],
                    "is_default": 1 if index == int(is_default_index) else 0
                }
                if v[4] == "0":
                    sku = self.gen_sku(prefix, attr_id)
                    temp["sku"] = sku
                    temp["created_time"] = datetime.datetime.now()
                    insert_values.append(temp)
                else:
                    temp["id"] = v[4]
                    update_values.append(temp)

            if insert_values or update_values:
                _ids, update_count = products.save_goods(_id, insert_values, update_values)
            redirect_url = u"{url}?id={id}&ed={is_edit}&category_id={category_id}".format(
                    url=self.reverse_url(".product_pictures"),
                    id=_id,
                    is_edit=req_data.get("is_edit", 0),
                    category_id=req_data.get("category_id", 0)
            )
            return self.make_write(result_code=0, result_data=redirect_url)

    @expose('/product/pictures.html', methods=('GET', 'POST'))
    @login_required
    def product_pictures(self):
        """
        货品图片
        :return:
        """
        if request.method == "GET":
            p_id = request.args.get("id", 0, type=int)
            is_edit = request.args.get("ed")
            category_id = request.args.get("category_id", 0, type=int)
            query_kwargs = {"id": p_id, "is_edit": is_edit, "category_id": category_id}
            picture_list = products.query_pictures_list(whats=u"id, label, image", product_id=p_id)

            return self.render(
                    template=u"product/pictures.html",
                    data=picture_list,
                    query_kwargs=query_kwargs
            )
        else:
            req_data = self.gen_arguments
            _id = req_data.get("id")  # 商品ID
            picture_id_list = req_data.getlist("picture_id")  # 图片ID列表
            cover_page_list = req_data.getlist("cover_page")  # 是否封面列表 0 代表封面 1 代表橱窗
            picture_url_list = req_data.getlist("picture_url")  # 图片url

            if cover_page_list and "0" not in cover_page_list:  # 如果未设置封面图，则默认拿第一张为封面图
                cover_page_list[0] = 0

            delete_values = [item for item in products.query_pictures_list(_id, "id, image")]  # 获取所有的picture

            insert_values = []
            update_values = []
            for index, v in enumerate(zip(cover_page_list, picture_url_list, picture_id_list), 1):
                temp = {
                    "label": int(v[0]),
                    "ordering": index,
                    "product_id": _id,
                }

                if v[2] != "0":
                    temp["id"] = v[2]
                    update_values.append(temp)
                else:
                    temp["image"] = v[1]
                    temp["created_time"] = datetime.datetime.now()
                    insert_values.append(temp)

            for pop_index in [index for index, i in enumerate(delete_values) for j in update_values
                              if i.get("id") == int(j.get("id"))]:  # 获取要删除的picture 信息
                delete_values[pop_index] = {}

            if insert_values or update_values:
                _ids, update_count = products.save_pictures(_id, insert_values, update_values,
                                                            [item["id"] for item in delete_values if item])
            redirect_url = u"{url}?id={id}&ed={is_edit}&category_id={category_id}".format(
                    url=self.reverse_url(".product_about"),
                    id=_id,
                    is_edit=req_data.get("is_edit", 0),
                    category_id=req_data.get("category_id", 0)
            )
            return self.make_write(result_code=0, result_data=redirect_url)

    @expose('/product/about.html', methods=('GET', 'POST'))
    @login_required
    def product_about(self):
        """
        图文介绍
        :return:
        """
        if request.method == "GET":
            p_id = request.args.get("id", 0, type=int)
            is_edit = request.args.get("ed")
            category_id = request.args.get("category_id", 0, type=int)
            query_kwargs = {"id": p_id, "is_edit": is_edit, "category_id": category_id}
            result = products.get_detail(whats="id, image_text, image_text_pad", _id=p_id)
            return self.render(
                template=u"product/product_about.html",
                data=result,
                query_kwargs=query_kwargs
            )
        else:
            req_data = self.gen_arguments
            _id = req_data.get("id")  # 货品ID
            editor_content = req_data.get("editorValue", "")
            editor_content_pad = req_data.get("editorValue_pad", "")
            is_edit = req_data.get("is_edit", 0, type=int)
            _update_value = dict(image_text=editor_content, image_text_pad=editor_content_pad)
            if not is_edit:
                _update_value["validity"] = 1
            else:
                validity = products.get_detail(whats=u"validity", _id=_id).validity
                _update_value["validity"] = 1 if validity == 2 else validity
            result = products.update(_id=_id, **_update_value)

            redirect_url = self.reverse_url(".list_view")
            return self.make_write(result_code=0, result_data=redirect_url)

    @expose('/product/delete.html', methods=('POST',))
    @login_required
    def delete_view(self):
        req_data = self.gen_arguments
        _id = req_data.get("id", 0)
        return_url = req_data.get("return_url", "")
        result = products.delete([_id])

        _handler_log.exception(u"[ProductDeleteHandler] id:{}, operator: {}".format(
                _id, self.current_operator))

        return self.make_write(result_code=0, result_data=self.decode_return_url(return_url))

    @expose('/product/detail.html', methods=('GET',))
    @login_required
    def detail_view(self):
        _id = request.args.get("id", 0, type=int)
        version = int(request.args.get("v", 1))
        return_url_str = request.args.get("return_url", "")
        if version == 1:
            result = products.get_detail(_id=_id)
            first_category_id = result.first_category
            second_category_id = result.second_category
            third_category_id = result.third_category
            category_ids = (first_category_id, second_category_id, third_category_id)
            category_result = category.get_category_by_id(*category_ids)
            category_name = u"{} / {} / {}".format(
                    category_result.get(first_category_id, ""),
                    category_result.get(second_category_id, ""),
                    category_result.get(third_category_id, "")
            )
            result["category_name"] = category_name
            supplier_detail = suppliers.get_detail(whats="fullname", _id=result.supplier_id)
            result["supplier_name"] = supplier_detail.fullname
            template_name = u"product/detail_basic.html"
        elif version == 2:
            result = list(products.query_goods_list(
                whats=u"sku, price, created_time, updated_time, stock, is_default, property_names",
                product_id=_id,
                filter_del=0
            ))

            for g in result:
                property_name_list = g.property_names.split("^")
                property_name = "  ".join(property_name_list)
                g["property_name"] = property_name
                g["price"] = float(g.price) / 100.0

            template_name = u"product/detail_goods.html"

        elif version == 3:
            result = products.query_pictures_list(whats=u"id, label, image", product_id=_id)
            template_name = u"product/detail_pictures.html"
        elif version == 4:
            result = products.get_detail(whats="image_text, image_text_pad", _id=_id)
            template_name = u"product/detail_about.html"

        return self.render(
                template=template_name,
                return_url_str=return_url_str,
                data=result,
                product_id=_id,
                return_url=self.decode_return_url(return_url_str)
        )

    @csrf.exempt
    @expose('/product/about/template.html', methods=('POST',))
    def product_about_template(self):
        """
        商品图文说明模板
        :return:
        """
        template_type = request.form.get("type", "title")
        tpl_name = u"{}.html".format(template_type)
        template_path = current_app.config.get("TEMPLATE_PATH")
        tpl_path = os.path.join(template_path, 'porduct_tpl', tpl_name)
        with open(tpl_path) as f:
            tpl_content = f.read()

        return self.make_write(result_code=0, result_data=tpl_content)

    @expose('/product/updown.html', methods=('POST',))
    @login_required
    def updown_view(self):
        """
        商品上架下架
        :return:
        """
        req_data = request.form.get("id").split("-")
        return_url = request.form.get("return_url", "")
        result = products.set_validity(ids=[req_data[0]], validity=req_data[1])
        return self.make_write(result_code=0, result_data=self.decode_return_url(return_url))

    @csrf.exempt
    @expose('/product/ajax/check.html', methods=('POST',))
    def check_view(self):
        """
        检查数据
        :return:
        """
        spu = request.date.get("spu", "")
        spu_info = products.get_detail(whats="id", spu=spu)
        result_code = 102 if spu_info else 0

        return self.make_write(result_code=result_code)
