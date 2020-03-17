# coding: utf-8
import logging

from flask import request
from flask.ext.admin import expose

from cores.actions import action
from cores.adminweb import BaseHandler
from dao.attributedao import attribute
from dao.categorydao import category
from extends import csrf
from libs.flask_login import login_required
from utils.helpers import utf8
from utils.verify import verify

__author__ = 'bin wen'

_log = logging.getLogger("ADMIN")
_handler_log = logging.getLogger("HANDLER")


class AttributeHandler(BaseHandler):
    """
    商品属性列表
    """
    column_list = ("name", "item_values", "category", "ordering", "updated_time")

    column_labels = {
        "name": u"属性名",
        "item_values": u"选项值",
        "category": u"所属分类",
        "updated_time": u"变更时间",
        "ordering": u"位置排序",
    }
    column_widget_args = {
        "updated_time": {'class': "hidden-480"}
    }
    tabs_list = (
        {"query_type": -1, "name": u"全部"},
    )

    @expose('/')
    @expose('/attribute/list.html')
    @login_required
    def list_view(self):
        page = request.args.get('page', 0, type=int)
        name = request.args.get('name', "")
        first_category_id = request.args.get('first_category_id', "")
        second_category_id = request.args.get('second_category_id', '')
        third_category_id = request.args.get('third_category_id', '')
        query_type = request.args.get('query_type', -1, type=int)

        query_kwargs = dict(
            name=name,
            first_category_id=first_category_id,
            second_category_id=second_category_id,
            third_category_id=third_category_id,
            query_type=query_type
        )

        def pager_url(p):
            if p is None:
                p = 0

            return self._get_url('.list_view', p, **query_kwargs)

        count = attribute.get_total_count(
                name=name,
                category_id=third_category_id
        )

        results = []
        num_pages = 0

        if count > 0:
            num_pages = self.gen_total_pages(count)
            if num_pages - 1 < page:
                page -= 1

            offset_value = page * self.page_size
            results = attribute.query_list(
                    name=name,
                    category_id=third_category_id,
                    limit=self.page_size,
                    offset=offset_value
            )

        actions, actions_confirmation = self.get_actions_list()
        return_url = self.gen_return_url(".list_view", page=page, **query_kwargs)

        return self.render(
            template="attribute/list.html",
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
            tabs_list=self.tabs_list
        )

    @expose('/attribute/action.html', methods=('POST',))
    @login_required
    def action_view(self):
        return_url = request.form.get("return_url", "")
        return self.handle_action(return_view=return_url)

    @action('delete', u"删除所选", u"你确定要删除所选的记录?")
    def action_delete(self, ids):
        try:
            result = attribute.delete(ids)
            _handler_log.info(u"[AttributeListHandler] batch delete, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as ex:
            _log.exception(u"[AttributeListHandler] batch delete error")

    @expose('/attribute/create.html', methods=('GET', 'POST'))
    @login_required
    def create_view(self):
        if request.method == "GET":
            return self.render("attribute/create.html")
        else:
            req_data = self.gen_arguments
            category_id = req_data.get("category_id", "")
            name = req_data.get("name", "")
            attribute_item = req_data.getlist("attribute_item_name")[:-1]

            if not verify.check_number(category_id):
                return self.make_write(result_code=2001)

            if not verify.check_name(name):
                return self.make_write(result_code=3001)

            if not attribute_item:
                return self.make_write(result_code=3002)
            else:
                for item in attribute_item:
                    if not verify.check_name(item):
                        return self.make_write(result_code=3002)

            result = attribute.save(
                category_id=category_id,
                name=name,
                attribute_item=attribute_item
            )
            return self.make_write(result_code=0, result_data=self.reverse_url(".list_view"))

    @expose('/attribute/edit.html', methods=('GET', 'POST'))
    @login_required
    def edit_view(self):
        if request.method == "GET":
            _id = request.args.get("id", "")
            return_url = request.args.get("return_url", "")
            result = attribute.get_detail(_id=_id)
            category_list = category.gen_full_category(result.category_id)
            result["category_list"] = category_list

            return self.render(
                    template="attribute/edit.html",
                    data=result,
                    return_url=return_url
            )
        else:
            req_data = self.gen_arguments
            return_url = req_data.get("return_url", "")
            _id = req_data.get("id")
            name = req_data.get("name", "")
            # 所有选项值
            attr_item_names = req_data.getlist("attribute_item_name")[:-1]
            # 要删除的ID
            del_item_ids = req_data.getlist("del_items")
            # 所有的ID
            attr_item_ids = req_data.getlist("attribute_item_id")[:-1]

            if not verify.check_number(_id):
                return self.make_write(result_code=100)

            if not verify.check_name(name):
                return self.make_write(result_code=3001)

            # 格式 [(tag, item_id,item_name)]  tag 0插入 1修改 2删除
            update_attr_items = []
            # 用于判断是否有可用的选项值
            is_check = 0

            if not attr_item_names:
                return self.make_write(result_code=3002)
            else:
                _id_names = zip(attr_item_ids, attr_item_names)
                for id_name in _id_names:
                    item_id = id_name[0]
                    item_name = id_name[1]
                    if item_id in del_item_ids:
                        update_attr_items.append((2, item_id, item_name))
                        continue

                    if not verify.check_name(item_name):
                        return self.make_write(result_code=3002)

                    is_check = 1
                    update_attr_items.append((0 if item_id in (0, "0") else 1, item_id, item_name))

            if not is_check:
                return self.make_write(result_code=3002)

            result = attribute.update(_id=_id, name=name, attribute_items=update_attr_items)
            return self.make_write(result_code=0, result_data=self.decode_return_url(return_url))

    @expose('/attribute/delete.html', methods=('POST',))
    @login_required
    def delete_view(self):
        req_data = self.gen_arguments
        return_url = req_data.get("return_url", "")
        _id = req_data.get("id")
        result = attribute.delete([_id])

        return self.make_write(result_code=0, result_data=self.decode_return_url(return_url))

    @expose('/attribute/detail.html', methods=('GET',))
    @login_required
    def detail_view(self):
        pass

    @csrf.exempt
    @expose('/attribute/ajax/check.html', methods=('POST',))
    def check_view(self):
        pass

