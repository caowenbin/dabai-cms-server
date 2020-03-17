# coding: utf-8
import logging

from flask import request
from flask.ext.admin import expose

from cores.actions import action
from cores.adminweb import BaseHandler
from dao.categorydao import category
from extends import csrf
from libs.flask_login import login_required
from utils.helpers import utf8
from utils.verify import verify

__author__ = 'bin wen'

_log = logging.getLogger("ADMIN")
_handler_log = logging.getLogger("HANDLER")


class CategoryHandler(BaseHandler):
    """
    分类列表
    """
    column_list = ("name", "validity", "created_time", "updated_time")

    column_labels = {
        "name": u"分类名称",
        "validity": u"状态",
        "updated_time": u"变更时间",
        "created_time": u"创建时间",
    }
    column_widget_args = {}
    tabs_list = (
        {"query_type": -1, "name": u"全部分类"},
        {"query_type": 1, "name": u"有效的"},
        {"query_type": 0, "name": u"已作废"},
    )

    @expose('/')
    @expose('/category/list.html')
    @login_required
    def list_view(self):
        page = request.args.get('page', 0, type=int)

        category_name = request.args.get("name", "")
        query_type = request.args.get("query_type", -1, type=int)
        parent_id_str = request.args.get("parent_id", "0-0")
        parent_ids = parent_id_str.split("-")
        parent_id = int(parent_ids[1])  # 父类ID
        first_parent_id = int(parent_ids[0])  # 根父类ID
        parent_data = {}
        if parent_id == 0:
            page_type = "first"
        elif first_parent_id == 0 and parent_id != 0:
            page_type = "second"
            parent_info = category.get_category_by_id(parent_id)
            parent_data["first"] = {"name": parent_info.get(parent_id, ""), "id": parent_id}
        else:
            page_type = "third"
            parent_info = category.get_category_by_id(parent_id, first_parent_id)
            parent_data["first"] = {"name": parent_info.get(first_parent_id, ""), "id": first_parent_id}
            parent_data["second"] = {"name": parent_info.get(parent_id, ""), "id": parent_id}

        query_kwargs = dict(name=category_name, query_type=query_type, parent_id=parent_id_str)

        def pager_url(p):
            if p is None:
                p = 0

            return self._get_url('.list_view', p, **query_kwargs)

        count = category.get_total_count(name=category_name, query_type=query_type, parent_id=parent_id)

        results = []
        num_pages = 0

        if count > 0:
            num_pages = self.gen_total_pages(count)
            if num_pages - 1 < page:
                page -= 1

            offset_value = page * self.page_size
            results = category.query_list(
                name=category_name,
                query_type=query_type,
                parent_id=parent_id,
                limit=self.page_size,
                offset=offset_value
            )

        actions, actions_confirmation = self.get_actions_list()
        return_url = self.gen_return_url(".list_view", page=page, **query_kwargs)
        template_name = u"category/{}_category_list.html".format(page_type)

        return self.render(
            template=template_name,
            actions=actions,
            actions_confirmation=actions_confirmation,
            count=count,
            page=page,
            num_pages=num_pages,
            pager_url=pager_url,
            data=results,
            query_kwargs=query_kwargs,
            return_url=return_url,
            parent_data=parent_data,
            column_list=self.column_list,
            column_labels=self.column_labels,
            column_widget_args=self.column_widget_args,
            tabs_list=self.tabs_list
        )

    @expose('/category/action.html', methods=('POST',))
    @login_required
    def action_view(self):
        return_url = request.form.get("return_url", "")
        return self.handle_action(return_view=return_url)

    @action('disable', u"注销(下架)所选", u"你确定要注销(下架)所选的记录?")
    def action_disable(self, ids):
        try:
            result = category.set_validity(ids, validity=0)
            _handler_log.info(u"[AdminListHandler] batch disable, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[AdminListHandler] batch disable error")

    @action('activate', u"激活(上架)选择", u"你确定要激活所选的记录?")
    def action_activate(self, ids):
        try:
            result = category.set_validity(ids, validity=1)
            _handler_log.info(u"[AdminListHandler] batch activate, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[AdminListHandler] batch activate error.")

    @expose('/category/create.html', methods=('GET', 'POST'))
    @login_required
    def create_view(self):
        if request.method == "GET":
            parent_id = request.args.get('parent_id', 0, type=int)
            return_url = request.args.get("return_url", "")
            data = {"parent_id": parent_id, "return_url": return_url}
            return self.render(template="category/create.html", data=data)
        else:
            req_data = self.gen_arguments
            parent_id = req_data.get('parent_id', 0, type=int)
            category_name = req_data.get("category_name", "")
            return_url = req_data.get("return_url", "")
            if not verify.check_name(category_name):
                return self.make_write(result_code=2002)

            result = category.save(name=category_name, parent_id=parent_id)
            _url = (self.decode_return_url(return_url)
                    if return_url else self.reverse_url(".list_view"))
            return self.make_write(result_code=0, result_data=_url)

    @expose('/category/edit.html', methods=('GET', 'POST'))
    @login_required
    def edit_view(self):
        if request.method == "GET":
            _id = request.args.get("id", "")
            return_url = request.args.get("return_url", "")
            result = category.get_detail(_id)
            return self.render(
                    template="category/edit.html",
                    data=result,
                    return_url=return_url
            )
        else:
            req_data = self.gen_arguments
            return_url = req_data.get("return_url", "")
            _id = req_data.get("id")
            category_name = req_data.get("category_name")

            result = category.update(_id=_id, name=category_name)

            return self.make_write(result_code=0, result_data=self.decode_return_url(return_url))

    @expose('/category/delete.html', methods=('POST',))
    @login_required
    def delete_view(self):
        pass

    @expose('/category/updown.html', methods=('POST',))
    @login_required
    def updown_view(self):
        """
        分类上架下架
        :return:
        """
        req_data = self.gen_arguments

        action_ids = req_data.get("id").split("-")
        return_url = req_data.get("return_url", "")
        _id = action_ids[0]
        validity = action_ids[1]
        result = category.set_validity(ids=[_id], validity=validity)
        _url = self.decode_return_url(return_url) if return_url else self.reverse_url("category")
        _handler_log.info(u"[CategoryUpDownHandler] id:{}, validity:{}, operator: {}".format(
                    _id, validity, self.current_operator)
            )
        return self.make_write(result_code=0, result_data=_url)

    @expose('/category/detail.html', methods=('GET',))
    @login_required
    def detail_view(self):
        pass

    @csrf.exempt
    @expose('/category/ajax/check.html', methods=('POST',))
    def check_view(self):
        pass

    @csrf.exempt
    @expose('/category/child.html', methods=('POST',))
    def child_view(self):
        """
        获取子类数据,即三级联动所用
        :return:
        """
        parent_id = request.form.get('parent_id', "")
        if parent_id == "":
            return self.make_write(result_code=100)

        child_category = category.query_child_category(parent_id=parent_id)
        return self.make_write(result_code=0, result_data=child_category)