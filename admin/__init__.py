#!/usr/bin/env python
# coding: utf8
from flask import Blueprint

from admin.administrators import AdministratorsHandler
from admin.attribute_admin import AttributeHandler
from admin.banner_admin import BannerHandler
from admin.brand_admin import BrandHandler
from admin.category_admin import CategoryHandler
from admin.channel_admin import ChannelHandler
from admin.city_admin import CityHandler
from admin.cornermark_admin import CornerMarkHandler
from admin.group_admin import GroupHandler
from admin.login import LoginOutHandler
from admin.order_admin import OrderHandler
from admin.product_admin import ProductHandler
from admin.refund_admin import RefundHandler
from admin.select import ContentSelectHandler
from admin.supplier_admin import SupplierHandler

from admin.upload import UploadHandler
from home import HomeHandler
from extends import admin

admin_blues = Blueprint('admin', __name__)
admin.add_view(LoginOutHandler(name=u"登录", endpoint="auth", url="/", is_menu=False))
admin.add_view(HomeHandler(name=u"个人中心", endpoint='home', menu_icon_value="icon-home"))
admin.add_view(AdministratorsHandler(name=u"管理员配置", endpoint='administrator', menu_icon_value="icon-group"))
admin.add_view(SupplierHandler(name=u"供应商管理", endpoint='supplier', menu_icon_value="icon-sitemap"))
admin.add_view(CityHandler(name=u"配送城市管理", endpoint='city', menu_icon_value="icon-truck"))
admin.add_view(CategoryHandler(name=u"分类管理", endpoint='category', menu_icon_value="icon-cogs"))
admin.add_view(AttributeHandler(name=u"属性管理", endpoint='attribute', menu_icon_value="icon-bookmark"))
admin.add_view(ChannelHandler(name=u"渠道管理", endpoint='channel', menu_icon_value="icon-plane"))
admin.add_view(BrandHandler(name=u"品牌管理", endpoint='brand', menu_icon_value="icon-btc"))
admin.add_view(CornerMarkHandler(name=u"角标管理", endpoint='cornermark', menu_icon_value="icon-tags"))
admin.add_view(BannerHandler(name=u"轮播图管理", endpoint='banner', menu_icon_value="icon-picture"))
admin.add_view(ProductHandler(name=u"商品管理", endpoint='product', menu_icon_value="icon-barcode"))
admin.add_view(GroupHandler(name=u"频道管理", endpoint='group', menu_icon_value="icon-folder-open"))
admin.add_view(OrderHandler(name=u"订单管理", endpoint='order', menu_icon_value="icon-cny"))
admin.add_view(RefundHandler(name=u"退款管理", endpoint='refund', menu_icon_value="icon-jpy"))
admin.add_view(UploadHandler(name=u"上传功能", endpoint='uploader', is_menu=False))
admin.add_view(ContentSelectHandler(name=u"模板内容下拉框", endpoint='content_select', is_menu=False))