# coding: utf-8
from dao.attributedao import attribute
from dao.bannerdao import banner
from dao.branddao import brands
from dao.channeldao import channel
from dao.groupdao import groups
from dao.productdao import products
from dao.supplierdao import suppliers

__author__ = 'bin wen'


class DataFlow(object):
    """
    公共的数据流
    """
    @staticmethod
    def gen_bind_banner():
        """
        绑定焦点图页面
        :return:
        """
        banner_list = list(banner.query_list(query_type=1, whats="id, name, image"))

        return banner_list

    @staticmethod
    def gen_bind_products():
        """
        绑定商品数据
        :return:
        """
        product_list = products.query_list(whats=u"id, title", query_type=1)
        return product_list

    @staticmethod
    def gen_bind_tweets():
        """
        绑定推文文章数据
        数据格式:[{"id":1, "title":"不错"}]
        :return:
        """
        tweet_list = []
        return tweet_list

    @staticmethod
    def gen_channels(query_type=1):
        """
        所有有效的渠道
        :param query_type:
        :return:
        """
        channel_list = channel.query_list(whats=u"channel_code, name", query_type=query_type)
        return channel_list

    @staticmethod
    def gen_template_code(is_list=True):
        """
        模板编码
        :param is_list:
        :return:
        """
        templates = {
            "T-001": {"code": "T-001",
                      "name": u"模板1",
                      "desc": u"轮播图模板,最多添加10张图片",
                      "tpl": u"t001.jpg"
                      },
            "T-002": {"code": "T-002",
                      "name": u"模板2",
                      "desc": u"显示标题及价格的二排四列的列表",
                      "tpl": u"t002.jpg"
                      },
            "T-003": {"code": "T-003",
                      "name": u"模板3",
                      "desc": u"左大图右4小图相结合列表",
                      "tpl": u"t003.jpg"
                      },
            "T-004": {"code": "T-004",
                      "name": u"模板4",
                      "desc": u"只显示图片二排三列的列表",
                      "tpl": u"t004.jpg"
                      },
            "T-005": {"code": "T-005",
                      "name": u"模板5",
                      "desc": u"图文模式,左文右图",
                      "tpl": u"t005.jpg"
                      },

            "T-006": {"code": "T-006",
                      "name": u"模板6",
                      "desc": u"用于分页瀑布流的,主要绑定商品分类",
                      "tpl": u"t006.jpg"
                      }
        }

        return templates.values() if is_list else templates

    @staticmethod
    def gen_banner_type():
        """
        获取焦点图类型
        数据格式如下:
        {0: u"商品", 1: u"文章", 2: u"外部url", 3: u"频道"}
        :return:
        """
        return {0: u"商品"}

    @staticmethod
    def gen_bind_groups():
        """
        有效的可绑定频道数据
        :return:
        """
        group_list = groups.query_list(
                whats=u"id, group_code as title",
                is_show_channel=False,
                query_type=1
        )
        return group_list

    @staticmethod
    def gen_suppliers(query_type=1):
        """
        获得对应的供应商
        :param query_type:
        :return:
        """
        supplier_list = suppliers.query_list(whats=u"id, short_name as name", query_type=query_type)
        return supplier_list

    @staticmethod
    def gen_brands():
        """
        获得对应的品牌
        :param query_type:
        :return:
        """
        brand_list = brands.query_list(whats=u"id, name")
        return brand_list

    @staticmethod
    def gen_product_properties(category_id):
        """
        获取商品属性及选项值
        :param category_id:
        :return:
        """
        active_attribute = attribute.get_active_attribute(category_id)
        return active_attribute

flow_tools = DataFlow
