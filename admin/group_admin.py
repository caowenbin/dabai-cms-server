# coding: utf-8
import logging


import uuid

from _mysql_exceptions import IntegrityError
from flask import request
from flask.ext.admin import expose

from cores.actions import action
from cores.adminweb import BaseHandler
from dao.categorydao import category
from dao.channeldao import channel
from dao.cornerdao import cornermark
from dao.groupdao import groups
from dao.productdao import products
from extends import csrf
from libs.flask_login import login_required
from utils.function_data_flow import flow_tools
from utils.helpers import utf8

__author__ = 'bin wen'

_log = logging.getLogger("ADMIN")
_handler_log = logging.getLogger("HANDLER")


class GroupHandler(BaseHandler):
    """
    频道列表
    """
    column_list = ("group_code", "name", "channels", "is_home", "ordering", "validity",
                   "updated_time")

    column_labels = {
        "group_code": u"频道编码",
        "name": u"频道名称",
        "channels": u"渠道",
        "validity": u"状态",
        "updated_time": u"变更时间",
        "ordering": u"排序",
        "is_home": u"是否首页"
    }
    column_widget_args = {}
    tabs_list = (
        {"query_type": -1, "name": u"全部"},
        {"query_type": 1, "name": u"上线中"},
        {"query_type": 0, "name": u"已下线"}
    )

    @expose('/')
    @expose('/group/list.html')
    @login_required
    def list_view(self):
        page = request.args.get('page', 0, type=int)
        name = request.args.get("name", "")
        group_code = request.args.get("group_code", "")
        channel_code = request.args.get("channel_code", "")
        start_time = request.args.get("start_time", "")
        end_time = request.args.get("end_time", "")
        query_type = request.args.get("query_type", -1, type=int)
        query_kwargs = dict(
                name=name,
                group_code=group_code,
                query_type=query_type,
                channel_code=channel_code,
                start_time=start_time,
                end_time=end_time
        )

        def pager_url(p):
            if p is None:
                p = 0

            return self._get_url('.list_view', p, **query_kwargs)

        count = groups.get_total_count(**query_kwargs)
        results = []
        num_pages = 0

        if count > 0:
            num_pages = self.gen_total_pages(count)
            if num_pages - 1 < page:
                page -= 1

            offset_value = page * self.page_size
            results = groups.query_list(
                    limit=self.page_size,
                    offset=offset_value,
                    **query_kwargs
            )

        actions, actions_confirmation = self.get_actions_list()
        return_url = self.gen_return_url(".list_view", page=page, **query_kwargs)
        return self.render(
            template="group/list.html",
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
            channel_codes=flow_tools.gen_channels(query_type=-1)
        )

    @expose('/group/action.html', methods=('POST',))
    @login_required
    def action_view(self):
        return_url = request.form.get("return_url", "")
        return self.handle_action(return_view=return_url)

    @action('disable', u"注销(下架)所选", u"你确定要注销(下架)所选的记录?")
    def action_disable(self, ids):
        try:
            result = groups.set_validity(ids, validity=0)
            _handler_log.info(u"[AdminListHandler] batch disable, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[AdminListHandler] batch disable error")

    @action('activate', u"激活(上架)选择", u"你确定要激活所选的记录?")
    def action_activate(self, ids):
        try:
            result = groups.set_validity(ids, validity=1)
            _handler_log.info(u"[AdminListHandler] batch activate, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[AdminListHandler] batch activate error.")

    @action('delete', u"删除所选", u"你确定要删除所选的记录?")
    def action_delete(self, ids):
        try:
            result = groups.delete(ids)
            _handler_log.info(u"[GroupList] batch delete, id:{}, operator: {}".format(
                    utf8(ids), self.current_operator)
            )
            return result
        except Exception as e:
            _log.exception(u"[GroupList] batch delete error:{}".format(e.message))

    @expose('/group/templates.html', methods=('GET',))
    @login_required
    def group_template_view(self):
        """
        模板
        :return:
        """
        template_list = flow_tools.gen_template_code()
        template_list.sort(key=lambda t: t["code"])
        return self.render(template="group/tpl.html", data=template_list)

    @expose('/group/create.html', methods=('GET', 'POST'))
    @login_required
    def create_view(self):
        if request.method == "GET":
            channel_list = flow_tools.gen_channels()
            return self.render(template="group/create_basic.html", data=channel_list)
        else:
            req_data = self.gen_arguments
            group_code = req_data.get("group_code", "")
            verify_code = self.verify_group_code(group_code)
            # if verify_code != 0:
            #     return self.make_write(result_code=verify_code, result_msg=u"频道编码重复")

            name = req_data.get("name", "")
            is_home = req_data.get("is_home")
            validity = req_data.get("validity")
            ordering = req_data.get("ordering", "1")
            # 渠道数据
            channel_codes = req_data.getlist("channel_code")
            # 模板的数据
            column_names = req_data.getlist("column_name")
            is_show_names = req_data.getlist("is_show_name")
            is_show_icons = req_data.getlist("is_show_icon")
            column_icons = req_data.getlist("icon_url")
            template_code = req_data.getlist("tpl_code")
            tpl_contents = zip(is_show_names, column_names, is_show_icons, column_icons, template_code)
            try:
                group_id, group_channel_ids, group_tpl_ids = groups.save(
                        group_code=group_code,
                        name=name,
                        is_home=is_home,
                        validity=validity,
                        ordering=ordering,
                        channel_codes=channel_codes,
                        group_templates=tpl_contents
                )
            except IntegrityError, e:
                _handler_log.warning(u"[GroupCreate] group_code:{} is exist".format(group_code))
                return self.make_write(result_code=verify_code, result_msg=u"频道编码重复")
            except Exception, e:
                _handler_log.exception(u"[GroupCreate] error:{}".format(e.message))
                return self.make_write(result_code=101)

            redirect_url = u"{url}?id={id}".format(
                    url=self.reverse_url(".template_bind_content_view"),
                    id=group_id
            )
            return self.make_write(result_code=0, result_data=redirect_url)

    def render_base_template(self, group_id):
        """
        频道模板主页面
        :param group_id:
        :return:
        """
        template_contents = groups.get_group_template_detail(
            whats=u"id,column_name,group_id,template_code, ordering",
            group_id=group_id
        )
        sys_methods = dict(random_uuid=uuid.uuid1)

        return self.render(template="group/template_contents.html",
                           data=template_contents,
                           group_id=group_id,
                           sys_methods=sys_methods
                           )

    def render_bind_content_template(self, filter_values):
        """
        绑定商品\焦点图\文章的页面
        :param filter_values:
        :return:
        """
        _values = filter_values.split("|")

        group_id = _values[0]
        template_content_id = _values[2]
        group_template_id = _values[1]
        tpl_type = _values[3]
        ordering = _values[4]
        img_size = _values[5]

        result = dict(group_template_id=group_template_id, group_id=group_id, ordering=ordering,
                      img_size=img_size)
        if template_content_id not in (0, "0"):
            template_content_detail = groups.get_template_content_detail(
                    _id=template_content_id)
        else:
            template_content_detail = {}

        result["template_content_detail"] = template_content_detail

        if tpl_type == "banner":
            banner_list = flow_tools.gen_bind_banner()
            result["banner_list"] = banner_list
            template_name = "group/bind_banners.html"
        elif tpl_type == "product":
            corner_mark_list = cornermark.query_group_name_list()
            result["corner_mark_list"] = corner_mark_list
            result["content_types"] = [{"code": 0, "name": u"商品"}, {"code": 2, "name": u"文章"}]
            content_type = template_content_detail.get("content_type", 0)
            if content_type == 0:
                select_content_list = flow_tools.gen_bind_products()
            else:
                select_content_list = flow_tools.gen_bind_tweets()

            result["select_content_list"] = select_content_list
            template_name = "group/bind_content.html"

        return self.render(template=template_name, data=result)

    def render_bind_category_template(self, filter_values):
        """
        绑定分类的页面
        :param filter_values:
        :return:
        """
        _values = filter_values.split("|")

        group_id = _values[0]
        group_template_id = _values[1]

        result = dict(group_template_id=group_template_id, group_id=group_id)
        template_content_list = groups.query_template_contents(u"content_code", group_template_id)
        content_codes = []
        for c in template_content_list:
            content_codes = [int(_id) for _id in c.content_code.split(";") if _id]
            break
        category_list = []
        first_categories = category.query_list(query_type=1, whats="id, name", parent_id=0)
        for fc in first_categories:
            second_categories = category.query_list(query_type=1, whats="id, name", parent_id=fc.id)
            is_pass = False
            is_first_checked = None
            for sc in second_categories:
                third_categories = category.query_list(query_type=1, whats="id, name", parent_id=sc.id)
                if not third_categories:
                    continue
                is_pass = True
                is_second_checked = None
                for tc in third_categories:
                    if tc.id in content_codes:
                        is_second_checked = 1
                        is_first_checked = 1
                        checked = "true"
                    else:
                        checked = "false"
                    category_list.append(
                        {"id": tc.id,
                         "pId": sc.id,
                         "name": tc.name,
                         "data": 3,
                         "checked": checked
                         }
                    )

                category_list.append(
                    {"id": sc.id,
                     "pId": fc.id,
                     "name": sc.name,
                     "data": 2,
                     "checked": "false" if is_second_checked is None else "true"
                     }
                )

            if is_pass:
                category_list.append(
                    {"id": fc.id,
                     "pId": 0,
                     "name": fc.name,
                     "data": 1,
                     "checked": "false" if is_first_checked is None else "true"
                     }
                )

        result["category_list"] = category_list
        template_name = "group/bind_category.html"

        return self.render(template=template_name, data=result)

    def content_handle(self):
        """
        处理除分类之外内容
        :return:
        """
        req_data = self.gen_arguments
        group_id = req_data.get("group_id")
        group_template_id = req_data.get("group_template_id")
        _id = req_data.get("id")
        content_code = req_data.get("content_code")
        content_type = req_data.get("content_type")
        ordering = req_data.get("ordering", 0)

        custom_title = req_data.get("custom_title", "")
        remark = req_data.get("remark", "")
        custom_image = req_data.get("custom_image", "")
        custom_image_size = req_data.get("custom_image_size", "")
        corner_mark_image = req_data.get("corner_mark_image", "")
        # 发布方式 1立即 0定时
        send_time_type = req_data.get("time", 1)
        if send_time_type == "0":
            start_time = req_data.get("start_time")
            end_time = req_data.get("end_time")
        else:
            start_time = None
            end_time = None
        if content_type == "0":
            if not custom_image:
                product_img_info = products.query_pictures_list(
                    product_id=content_code,
                    whats="image",
                    label=0
                )
                for p in product_img_info:
                    custom_image = p.image
                    break

            if not custom_title:
                product_info = products.get_detail(whats=u"short_name", _id=content_code)
                custom_title = product_info.short_name

        _values = dict(
            group_template_id=group_template_id,
            content_type=content_type,
            content_code=content_code,
            custom_title=custom_title,
            remark=remark,
            custom_image=custom_image,
            custom_image_size=custom_image_size,
            corner_mark_image=corner_mark_image if corner_mark_image != "0" else "",
            start_time=start_time if start_time else None,
            end_time=end_time if end_time else None,
            ordering=ordering,
            group_id=group_id
        )
        if corner_mark_image == "":
            _values["corner_mark_image"] = None

        if _id == "0":
            result = groups.save_template_content_detail(**_values)
        else:
            result = groups.update_template_content_detail(_id=_id, **_values)

        return result

    def template_category_handle(self):
        """
        绑定分类
        :return:
        """
        req_data = self.gen_arguments
        group_id = req_data.get("group_id")
        group_template_id = req_data.get("group_template_id")
        category_names = req_data.get("category_names", "")[:-1]
        categories = req_data.get("categories", "")[:-1]

        result = groups.save_template_category_detail(group_template_id, group_id, categories, category_names)

        return result

    @expose('/group/template/bind/content.html', methods=('GET', 'POST'))
    @login_required
    def template_bind_content_view(self):
        """
        模板绑定内容
        :return:
        """
        if request.method == "GET":
            group_id = request.args.get("id", None)
            # 绑定分类的页面请求
            request_page_type = request.args.get("page_type", "base")
            filter_values = request.args.get("data", "")  # 查询条件(频道ID|频道模板ID|模板内容ID|请求类型)
            if request_page_type == "base":
                return self.render_base_template(group_id=group_id)
            elif request_page_type == "content":
                return self.render_bind_content_template(filter_values=filter_values)
            elif request_page_type == "category":
                return self.render_bind_category_template(filter_values=filter_values)
        else:
            req_data = self.gen_arguments
            page_type = req_data.get("page_type", "base")
            group_id = req_data.get("group_id")

            if page_type != "category":
                result = self.content_handle()
            elif page_type == "category":
                result = self.template_category_handle()

            redirect_url = u"{url}?id={id}".format(
                    url=self.reverse_url(".template_bind_content_view"),
                    id=group_id
            )
            return self.make_write(result_code=0, result_data=redirect_url)

    @expose('/group/edit.html', methods=('GET', 'POST'))
    @login_required
    def edit_view(self):
        """
        修改基本信息
        :return:
        """
        if request.method == "GET":
            _id = request.args.get("id", "")
            result = groups.get_detail(_id=_id, is_show_template=True)
            channel_list = flow_tools.gen_channels()

            return self.render(
                    template="group/edit_basic.html",
                    data=result,
                    channel_list=channel_list,
                    template_code_list=flow_tools.gen_template_code(is_list=False)
            )
        else:
            req_data = self.gen_arguments
            _id = req_data.get("id")
            group_code = req_data.get("group_code", "")
            name = req_data.get("name", "")
            is_home = req_data.get("is_home")
            validity = req_data.get("validity")
            ordering = req_data.get("ordering", "1")
            # 渠道数据
            channel_codes = req_data.getlist("channel_code")
            # 模板的数据
            group_template_ids = req_data.getlist("group_template_id")
            column_names = req_data.getlist("column_name")
            is_show_names = req_data.getlist("is_show_name")
            is_show_icons = req_data.getlist("is_show_icon")
            column_icons = req_data.getlist("icon_url")
            template_code = req_data.getlist("tpl_code")
            tpl_contents = zip(is_show_names, column_names, is_show_icons, column_icons, template_code,
                               group_template_ids)
            result = groups.update(
                _id=_id,
                group_code=group_code,
                name=name,
                is_home=is_home,
                validity=validity,
                ordering=ordering,
                channel_codes=channel_codes,
                group_templates=tpl_contents
            )
            redirect_url = u"{url}?id={id}".format(
                    url=self.reverse_url(".template_bind_content_view"),
                    id=_id
            )
            return self.make_write(result_code=0, result_data=redirect_url)

    @expose('/group/template/content/delete.html', methods=('POST',))
    @login_required
    def delete_template_content_view(self):
        """
        删除模板的内容
        :return:
        """
        req_data = self.gen_arguments
        _values = req_data.get("v", "").split("|")

        group_id = _values[0]
        template_content_id = _values[2]
        result = groups.delete_template_content(_id=template_content_id)
        redirect_url = u"{url}?id={id}".format(
                url=self.reverse_url(".template_bind_content_view"),
                id=group_id
        )
        return self.make_write(result_code=0, result_data=redirect_url)

    @expose('/group/delete.html', methods=('POST',))
    @login_required
    def delete_view(self):
        req_data = self.gen_arguments
        _id = req_data.get("id", 0, type=int)
        return_url = req_data.get("return_url", "")
        result = groups.delete([_id])
        _handler_log.info(u"[GroupDeleteHandler] id:{}, operator: {}".format(
                    _id, self.current_operator)
        )
        return self.make_write(result_code=0, result_data=self.decode_return_url(return_url))

    @expose('/group/detail.html', methods=('GET',))
    @login_required
    def detail_view(self):
        _id = request.args.get("id", 0, type=int)
        version = request.args.get("v", 1, type=int)
        return_url_str = request.args.get("return_url", "")
        if version == 1:
            result = groups.get_detail(_id=_id, is_show_template=True)
            channel_codes = result.get("channels", [])
            if channel_codes:
                channel_names = channel.query_channel_by_code(channel_codes=channel_codes, whats=u"name")
            else:
                channel_names = []
            result["channel_names"] = [r.name for r in channel_names]

            return self.render(
                    template="group/detail_basic.html",
                    data=result,
                    return_url=self.decode_return_url(return_url_str),
                    template_code_list=flow_tools.gen_template_code(is_list=False),
                    return_url_str=return_url_str
            )
        else:
            template_contents = groups.get_group_template_detail(
                    whats=u"id,column_name,group_id,template_code, ordering",
                    group_id=_id
            )
            sys_methods = dict(random_uuid=uuid.uuid1)

            return self.render(
                    template="group/detail_template_contents.html",
                    data=template_contents,
                    group_id=_id,
                    sys_methods=sys_methods,
                    return_url=self.decode_return_url(return_url_str),
                    return_url_str=return_url_str
            )

    @csrf.exempt
    @expose('/group/ajax/check.html', methods=('POST',))
    def check_view(self):
        group_code = request.form.get("group_code")
        result_code = self.verify_group_code(group_code)

        return self.make_write(result_code=result_code)

    @staticmethod
    def verify_group_code(group_code):
        """
        检查频道编码唯一性
        :param group_code:
        :return:
        """
        group_info = groups.get_detail(whats="id", group_code=group_code, is_show_channel=False)
        return 102 if group_info else 0

    @csrf.exempt
    @expose('/group/template/content/updown.html', methods=('POST',))
    @login_required
    def updowntemplatecontent_view(self):
        """
        上下移动模板内容
        :return:
        """
        _values = request.form.get("v", "").split("|")
        _action = request.form.get("action")
        group_id = _values[0]
        template_content_id = _values[2]
        ordering = int(_values[4])
        if _action == "up":
            ordering -= 1
        else:
            ordering += 1
        result = groups.update_template_content_detail(_id=template_content_id, ordering=ordering)
        redirect_url = u"{url}?id={id}".format(
                url=self.reverse_url(".template_bind_content_view"),
                id=group_id
        )
        return self.make_write(result_code=0, result_data=redirect_url)
