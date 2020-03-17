# coding: utf8
import datetime
from operator import itemgetter

from extends import db
from dao.channeldao import channel

__author__ = 'bin wen'


class GroupDao(object):

    @staticmethod
    def save(**kwargs):
        """
        保存信息
        :param kwargs:
        :return:
        """
        group_code = kwargs.get("group_code")
        name = kwargs.get("name", '')
        is_home = kwargs.get("is_home")
        validity = kwargs.get("validity")
        ordering = kwargs.get("ordering")
        channel_codes = kwargs.get("channel_codes", [])
        group_templates = kwargs.get("group_templates", [])

        with db.master.transaction():
            now_time = datetime.datetime.now()
            group_id = db.master.insert(
                tablename="groups",
                created_time=now_time,
                group_code=group_code,
                name=name,
                is_home=is_home,
                validity=validity,
                ordering=ordering
            )
            channel_insert_vals = [dict(created_time=now_time, group_id=group_id, channel_code=code)
                                   for code in channel_codes]
            tpl_insert_vals = []
            for index, t in enumerate(group_templates, 1):
                # t的数据结构zip(is_show_names, column_names, is_show_icons, column_icons, template_code)
                tmp = dict(created_time=now_time,
                           group_id=group_id,
                           is_show_name=t[0],
                           column_name=t[1],
                           is_show_icon=t[2],
                           column_icon=t[3],
                           template_code=t[4],
                           ordering=index
                           )
                tpl_insert_vals.append(tmp)

            if channel_insert_vals:
                group_channel_ids = db.master.multiple_insert(
                        tablename="group_channels",
                        values=channel_insert_vals
                )
            if tpl_insert_vals:
                group_tpl_ids = db.master.multiple_insert(
                        tablename="group_templates",
                        values=tpl_insert_vals
                )

            return group_id, group_channel_ids, group_tpl_ids

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
        group_code = kwargs.get("group_code", "")
        group_ids = kwargs.get("group_ids")
        name = kwargs.get("name", "")
        start_time = kwargs.get("start_time")
        end_time = kwargs.get("end_time")

        if query_type != -1:  # 有效的
            wheres.append(u"validity=$validity")
            values["validity"] = query_type

        if name:
            wheres.append(u"name like $name")
            values["name"] = u"%{}%".format(name)

        if group_code:
            wheres.append(u"group_code like $group_code")
            values["group_code"] = u"%{}%".format(group_code)

        if group_ids:
            wheres.append(u"id in $group_ids")
            values["group_ids"] = group_ids

        if start_time:
            wheres.append(u"updated_time >= $start_time")
            values["start_time"] = start_time

        if end_time:
            wheres.append(u"updated_time <= $end_time")
            values["end_time"] = end_time

        where_str = u" and ".join(wheres) if wheres else None

        return where_str, values

    @staticmethod
    def query_group_channel(channel_code=None, group_ids=None):
        """
        查询频道的渠道
        :param channel_code:
        :param group_ids:
        :return:
        """
        group_channel_list = {}
        wheres = []
        values = dict()
        if channel_code:
            wheres.append(u"channel_code=$channel_code")
            values["channel_code"] = channel_code
        if group_ids:
            wheres.append(u"group_id in $group_ids")
            values["group_ids"] = group_ids

        where_str = u" and ".join(wheres) if wheres else None

        group_channel = db.slave.select(
            tables=u"group_channels",
            vars=values,
            where=where_str,
            what=u"channel_code, group_id"
        )

        for gc in group_channel:
            group_channel_list.setdefault(gc.group_id, []).append(gc.channel_code)

        return group_channel_list

    @staticmethod
    def query_list(whats=None, limit=None, offset=None, is_show_channel=True, **kwargs):
        """
        分页查询信息 query_type: 0全部 1有效 2注销
        :param whats:
        :param limit:
        :param offset:
        :param is_show_channel: 是否显示渠道
        :param kwargs:
        :return:
        """
        if is_show_channel:
            channel_code = kwargs.get("channel_code")
            group_channel_list = None
            if channel_code:
                group_channel_list = GroupDao.query_group_channel(channel_code=channel_code)
                kwargs["group_ids"] = group_channel_list.keys()

        where_str, values = GroupDao.__gen_wheres_values(**kwargs)
        if not whats:
            whats = u"id,group_code,name,is_home,ordering,validity,updated_time"

        results = list(db.slave.select(
            tables=u'groups',
            what=whats,
            vars=values,
            where=where_str,
            limit=limit,
            offset=offset,
            order=u"updated_time DESC"
        ))

        if is_show_channel:
            if not channel_code:
                group_ids = [r.id for r in results]
                group_channel_list = GroupDao.query_group_channel(group_ids=group_ids)
            for r in results:
                channel_codes = group_channel_list.get(r.id, [])
                if channel_codes:
                    channel_names = channel.query_channel_by_code(channel_codes=channel_codes, whats=u"name")
                else:
                    channel_names = []
                r["channels"] = [c.name for c in channel_names]

        return results

    @staticmethod
    def get_total_count(**kwargs):
        """
        获取对应的条数
        :param kwargs:
        :return:
        """
        channel_code = kwargs.get("channel_code")
        group_channel_list = {}
        if channel_code:
            group_channel = db.slave.select(
                tables=u"group_channels",
                where={"channel_code": channel_code},
                what=u"channel_code, group_id"
            )

            for gc in group_channel:
                group_channel_list.setdefault(gc.group_id, []).append(gc.channel_code)

        kwargs["group_ids"] = group_channel_list.keys()
        where_str, values = GroupDao.__gen_wheres_values(**kwargs)

        counts = db.slave.select(
            tables='groups',
            what="count(id) as counts",
            vars=values,
            where=where_str
        ).first().counts

        return counts

    @staticmethod
    def get_detail(whats="*", _id=None, group_code=None, is_show_template=False, is_show_channel=True):
        """
        详情
        :param whats:
        :param _id:
        :param group_code:
        :param is_show_template: 是否查询频道模板列表, 默认不显示
         :param is_show_channel: 是否查询频道渠道列表, 默认显示
        :return:
        """
        where = {}
        if _id is not None:
            where["id"] = _id
        if group_code is not None:
            where["group_code"] = group_code
        result = db.slave.select(tables=u"groups", where=where).first()

        if is_show_channel:
            group_id = result.id
            channel_list = GroupDao.query_group_channel(group_ids=[group_id])
            result["channels"] = channel_list.get(group_id, [])
        if is_show_template:
            template_content_list = GroupDao.get_group_template_detail(
                whats=u"column_name,id,template_code,is_show_name,column_icon,is_show_icon,ordering",
                group_id=group_id,
                is_show_content=False
            )
            result["template_list"] = template_content_list

        return result

    @staticmethod
    def get_template_content_detail(_id, whats="*"):
        """
        模板内容详情
        :param whats:
        :param _id:
        :return:
        """
        result = db.slave.select(tables=u"template_contents", where={"id": _id}).first()
        return result

    @staticmethod
    def __gen_template_content_values(**kwargs):
        """
        解析生成模板内容值
        :param kwargs:
        :return:
        """
        set_values = {}

        if "group_template_id" in kwargs:
            set_values["group_template_id"] = kwargs["group_template_id"]

        if "content_type" in kwargs:
            set_values["content_type"] = kwargs["content_type"]

        if "content_code" in kwargs:
            set_values["content_code"] = kwargs["content_code"]

        if "custom_title" in kwargs:
            set_values["custom_title"] = kwargs["custom_title"]

        if "remark" in kwargs:
            set_values["remark"] = kwargs["remark"]

        if "custom_image" in kwargs:
            set_values["custom_image"] = kwargs["custom_image"]

        if "custom_image_size" in kwargs:
            set_values["custom_image_size"] = kwargs["custom_image_size"]

        corner_mark_image = kwargs.get("corner_mark_image", None)
        if corner_mark_image is not None:
            set_values["corner_mark_image"] = corner_mark_image

        if "ordering" in kwargs:
            set_values["ordering"] = kwargs["ordering"]

        if "start_time" in kwargs:
            set_values["start_time"] = kwargs["start_time"]

        if "end_time" in kwargs:
            set_values["end_time"] = kwargs["end_time"]

        if "group_id" in kwargs:
            set_values["group_id"] = kwargs["group_id"]

        return set_values

    @staticmethod
    def save_template_content_detail(**kwargs):
        """
        保存模板内容信息
        :param kwargs:
        :return:
        """
        insert_values = GroupDao.__gen_template_content_values(**kwargs)
        insert_values["created_time"] = datetime.datetime.now()
        result = db.master.insert(tablename="template_contents", **insert_values)

        return result

    @staticmethod
    def save_template_category_detail(group_template_id, group_id, content_code, category_name):
        """
        保存模板绑定的分类信息
        :param group_template_id:
        :param group_id:
        :param content_code:
        :param category_name:
        :return:
        """
        with db.master.transaction():
            del_result = db.master.delete(
                table='template_contents',
                where={"group_template_id": group_template_id}
            )
            now_time = datetime.datetime.now()
            _insert_values = dict(
                created_time=now_time,
                group_id=group_id,
                group_template_id=group_template_id,
                content_code=content_code,
                content_type=3,
                custom_image=category_name
            )
            _ids = db.master.insert(tablename="template_contents", **_insert_values)

            return _ids

    @staticmethod
    def update_template_content_detail(_id, **kwargs):
        """
        修改模板内容信息
        :param _id:
        :param kwargs:
        :return:
        """
        set_values = GroupDao.__gen_template_content_values(**kwargs)
        result = db.master.update(tables='template_contents', where={'id': _id}, **set_values)

        return result

    @staticmethod
    def query_template_contents(whats=None, *group_template_id):
        """
        根据频道模板ID查询对应的值
        :param group_template_id:
        :param whats:
        :return:
        """
        if whats is None:
            whats = u"id, group_template_id, custom_image, ordering"

        if not group_template_id:
            return []
        content_list = db.slave.select(
            tables=u"template_contents",
            what=whats,
            where=u"group_template_id in $ids",
            vars={"ids": list(group_template_id)}
        )

        return content_list

    @staticmethod
    def get_group_template_ids(group_id):
        """
        获取频道所有对应的模板ID
        :param group_id:
        :return:
        """
        tpl_ids = db.slave.select(
            tables=u"group_templates",
            what=u"id",
            where={"group_id": group_id}
        )
        _ids = {o.id for o in tpl_ids}
        return _ids

    @staticmethod
    def get_group_template_detail(whats="*", group_id=None, is_show_content=True):
        """
        模板详情及模板内容
        :param whats:
        :param group_id:
        :param is_show_content: 是否展示具体模板内容,默认显示
        :return:
        """
        tpl_list = db.slave.select(
            tables=u"group_templates",
            what=whats,
            where={"group_id": group_id}
        )
        tpl_info = {t.id: t for t in tpl_list}

        if is_show_content:
            _ids = tpl_info.keys()
            content_list = GroupDao.query_template_contents(
                u"id, group_template_id, custom_image, ordering", *_ids
            )

            content_details = {}
            for c in content_list:
                group_template_id = c.group_template_id
                if group_template_id in content_details:
                    content_details[group_template_id][c.ordering] = dict(c)
                else:
                    content_details[group_template_id] = {c.ordering: dict(c)}
            for k, v in tpl_info.iteritems():
                v["childs"] = content_details.get(k, {})
        result = tpl_info.values()
        result.sort(key=itemgetter('ordering'))
        return result

    @staticmethod
    def update(_id, **kwargs):
        """
        修改信息
        :param _id:
        :param kwargs:
        :return:
        """
        name = kwargs.get("name", '')
        is_home = kwargs.get("is_home")
        validity = kwargs.get("validity")
        ordering = kwargs.get("ordering")
        channel_codes = kwargs.get("channel_codes", [])
        group_templates = kwargs.get("group_templates", [])

        with db.master.transaction():
            now_time = datetime.datetime.now()
            group_result = db.master.update(
                tables="groups",
                where={"id": _id},
                name=name,
                is_home=is_home,
                validity=validity,
                ordering=ordering
            )
            db.master.delete(table="group_channels", where={"group_id": _id})
            channel_insert_values = [dict(created_time=now_time, group_id=_id, channel_code=code)
                                     for code in channel_codes]
            tpl_insert_values = []  # 待插入的
            tpl_update_values = []  # 待修改
            tpl_del_values = []  # 待删除的
            # 获得数据库中频道所有的模板
            group_template_id_list = GroupDao.get_group_template_ids(group_id=_id)
            for index, t in enumerate(group_templates, 1):
                # t的数据结构zip(is_show_names, column_names, is_show_icons, column_icons,
                # template_code, group_template_ids)
                group_template_id = int(t[5])
                if group_template_id == 0:
                    tmp = dict(
                        created_time=now_time,
                        group_id=_id,
                        is_show_name=t[0],
                        column_name=t[1],
                        is_show_icon=t[2],
                        column_icon=t[3],
                        template_code=t[4],
                        ordering=index
                    )
                    tpl_insert_values.append(tmp)
                else:
                    if group_template_id in group_template_id_list:
                        #  修改
                        tmp = dict(
                            id=group_template_id,
                            is_show_name=t[0],
                            column_name=t[1],
                            is_show_icon=t[2],
                            column_icon=t[3],
                            template_code=t[4],
                            ordering=index
                        )
                        tpl_update_values.append(tmp)
                        group_template_id_list.remove(group_template_id)
                    else:
                        tpl_del_values.append(group_template_id)

            if group_template_id_list:
                tpl_del_values += group_template_id_list
            if channel_insert_values:
                db.master.multiple_insert(tablename="group_channels",values=channel_insert_values)
            if tpl_insert_values:
                group_tpl_ids = db.master.multiple_insert(
                    tablename="group_templates",
                    values=tpl_insert_values
                )
            if tpl_update_values:
                for v in tpl_update_values:
                    db.master.update(tables="group_templates", where={"id": v["id"]}, **v)

            if tpl_del_values:
                del_template_result, del_content_result = GroupDao.delete_group_templates(*tpl_del_values)

            return group_result

    @staticmethod
    def delete_group_templates(*group_template_id):
        """
        根据频道模板ID批量删除模板及其内容
        :param group_template_id:
        :return:
        """
        _ids = list(group_template_id)
        del_content_result = db.master.delete(
            table='template_contents',
            vars={'ids': _ids},
            where="group_template_id in $ids"
        )
        del_template_result = db.master.delete(
            table='group_templates',
            vars={'ids': _ids},
            where="id in $ids"
        )
        return del_template_result, del_content_result

    @staticmethod
    def delete(_ids):
        """
        批量删除频道
        :param _ids:
        :return:
        """
        with db.master.transaction():
            group_channel_result = db.master.delete(
                table='group_channels',
                vars={'ids': _ids},
                where="group_id in $ids"
            )
            group_template_content_result = db.master.delete(
                table='template_contents',
                vars={'ids': _ids},
                where="group_id in $ids"
            )
            group_template_result = db.master.delete(
                table='group_templates',
                vars={'ids': _ids},
                where="group_id in $ids"
            )
            group_result = db.master.delete('groups', vars={'ids': _ids}, where="id in $ids")

            return group_result

    @staticmethod
    def delete_template_content(_id):
        """
        根据模板内容ID删除模板内容
        :param _id:
        :return:
        """
        result = db.master.delete('template_contents', where={"id": _id})

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

        result = db.master.update('groups', vars={'ids': ids}, where="id in $ids ", **set_values)

        return result

    @staticmethod
    def get_group_templates(_ids=None, whats="*"):
        """
        获取频道和模板关联关系
        :param _ids:
        :param whats:
        :return:
        """

        if isinstance(_ids, list):
            values = {'ids': _ids}
            wheres = "group_id in $ids"

        result = db.slave.select(
            tables=u"group_templates",
            what=whats,
            vars=values,
            where=wheres
        )

        return result

    @staticmethod
    def get_template_content_list(_ids=None, whats="*"):
        """
        模板内容列表
        :param _ids:
        :param whats:
        :return:
        """
        wheres = None
        values = None
        if isinstance(_ids, list):
            values = {'ids': _ids}
            wheres = "group_id in $ids"

        result = db.slave.select(
            tables=u"template_contents",
            what=whats,
            vars=values,
            where=wheres
        )

        return result

    @staticmethod
    def get_groups_by_channel(channel_code, whats="*"):

        _sql = """
            select {whats} from group_channels as gc join groups as g on gc.group_id = g.id
             where g.validity = 1 and gc.channel_code = {channel_code}
        """.format(whats=whats, channel_code=channel_code)

        result = db.slave.execute_by_sql(_sql)
        return result

groups = GroupDao
