#!/usr/bin/env python
# coding: utf8
from utils.helpers import import_object
from admin import admin_blues


def init_admin_url(app):
    """
    初始化
    :param app:
    :return:
    """
    pass
    # app.add_url_rule(rule=r'/', view_func=import_object("admin.login.login"), methods=("POST", "GET"))

    # app.add_url_rule(rule=r'/home.html', view_func=import_object("admin.home.HomeHandler"), endpoint="home")

# urls = [(r"/", LoginHandler),
#         web.URLSpec(r"/login.html", LoginHandler, name="login"),
#         web.URLSpec(r"/logout.html", LogOutHandler, name="logout"),
#         web.URLSpec(r"/home.html", HomeHandler, name="home"),
#         web.URLSpec(r"/pwd.html", PasswordHandler, name="pwd"),
#
#         web.URLSpec(r"/admin/administrator/list.html", AdminListHandler, name="administrator"),
#         web.URLSpec(r"/admin/administrator/create.html", AdminCreateHandler, name="admin_create"),
#         web.URLSpec(r"/admin/administrator/edit.html", AdminEditHandler, name="admin_edit"),
#         web.URLSpec(r"/admin/administrator/delete.html", AdminDeleteHandler, name="admin_del"),
#         web.URLSpec(r"/admin/administrator/view.html", AdminViewHandler, name="admin_view"),
#         web.URLSpec(r"/admin/administrator/check.html", AdminCheckHandler, name="admin_check"),
#
#         web.URLSpec(r"/admin/attribute/list.html", AttributeListHandler, name="attribute"),
#         web.URLSpec(r"/admin/attribute/create.html", AttributeCreateHandler, name="attribute_create"),
#         web.URLSpec(r"/admin/attribute/edit.html", AttributeEditHandler, name="attribute_edit"),
#
#         web.URLSpec(r"/admin/banner/list.html", BannerListHandler, name="banner"),
#         web.URLSpec(r"/admin/banner/create.html", BannerCreateHandler, name="banner_create"),
#         web.URLSpec(r"/admin/banner/edit.html", BannerEditHandler, name="banner_edit"),
#
#         web.URLSpec(r"/admin/brand/list.html", BrandListHandler, name="brand"),
#         web.URLSpec(r"/admin/brand/create.html", BrandCreateHandler, name="brand_create"),
#         web.URLSpec(r"/admin/brand/delete.html", BrandDeleteHandler, name="brand_del"),
#
#         web.URLSpec(r"/admin/category/list.html", CategoryListHandler, name="category"),
#         web.URLSpec(r"/admin/category/create.html", CategoryCreateHandler, name="category_create"),
#         web.URLSpec(r"/admin/category/edit.html", CategoryEditHandler, name="category_edit"),
#         web.URLSpec(r"/admin/category/child.html", CategoryChildHandler, name="category_child"),
#         web.URLSpec(r"/admin/category/updown.html", CategoryUpDownHandler, name="category_updown"),
#
#         web.URLSpec(r"/admin/channel/list.html", ChannelListHandler, name="channel"),
#         web.URLSpec(r"/admin/channel/create.html", ChannelCreateHandler, name="channel_create"),
#         web.URLSpec(r"/admin/channel/delete.html", ChannelDeleteHandler, name="channel_del"),
#         web.URLSpec(r"/admin/channel/edit.html", ChannelEditHandler, name="channel_edit"),
#
#         web.URLSpec(r"/admin/city/list.html", CityListHandler, name="city"),
#
#         web.URLSpec(r"/admin/cornermark/list.html", CornerMarkListHandler, name="cornermark"),
#         web.URLSpec(r"/admin/cornermark/create.html", CornerMarkCreateHandler, name="cornermark_create"),
#         web.URLSpec(r"/admin/cornermark/delete.html", CornerMarkDeleteHandler, name="cornermark_del"),
#         web.URLSpec(r"/admin/cornermark/group/list.html", GroupCornerMarkListHandler, name="cornermark_group"),
#
#         web.URLSpec(r"/admin/group/list.html", GroupListHandler, name="group"),
#         web.URLSpec(r"/admin/group/create.html", GroupCreateHandler, name="group_create"),
#         web.URLSpec(r"/admin/group/edit.html", GroupEditHandler, name="group_edit"),
#         web.URLSpec(r"/admin/group/delete.html", GroupDeleteHandler, name="group_del"),
#         web.URLSpec(r"/admin/group/template/list.html", BindContentHandler, name="group_bind_content"),
#         web.URLSpec(r"/admin/group/templates.html", GroupTemplateHandler, name="group_tpl"),
#         web.URLSpec(r"/admin/group/template/content/delete.html", DeleteTemplateContentHandler, name="content_del"),
#         web.URLSpec(r"/admin/group/template/content/updown.html", UpDownTemplateContentHandler, name="content_updown"),
#         web.URLSpec(r"/admin/group/view.html", GroupViewHandler, name="group_view"),
#         web.URLSpec(r"/admin/group/check.html", GroupCheckHandler, name="group_check"),
#
#         web.URLSpec(r"/admin/order/list.html", OrderListHandler, name="order"),
#         web.URLSpec(r"/admin/order/detail.html", OrderDetailHandler, name="order_detail"),
#         web.URLSpec(r"/admin/order/send.html", OrderSendHandler, name="order_send"),
#         web.URLSpec(r"/admin/order/cancel.html", OrderCancelHandler, name="order_cancel"),
#
#         web.URLSpec(r"/admin/product/list.html", ProductListHandler, name="product"),
#         web.URLSpec(r"/admin/product/create.html", ProductCreateHandler, name="product_create"),
#         web.URLSpec(r"/admin/product/edit.html", ProductEditHandler, name="product_edit"),
#         web.URLSpec(r"/admin/product/attributes.html", GoodsHandler, name="product_attributes"),
#         web.URLSpec(r"/admin/product/pictures.html", ProductPicturesHandler, name="product_pictures"),
#         web.URLSpec(r"/admin/product/about.html", ProductAboutHandler, name="product_about"),
#         web.URLSpec(r"/admin/product/delete.html", ProductDeleteHandler, name="product_del"),
#         web.URLSpec(r"/admin/product/view.html", ProductViewHandler, name="product_view"),
#         web.URLSpec(r"/admin/product/detail/templates.html", ProductTemplateHandler, name="product_templates"),
#         web.URLSpec(r"/admin/product/downup.html", ProductDownUpHandler, name="product_downup"),
#         web.URLSpec(r"/admin/product/check.html", ProductCheckHandler, name="product_check"),
#
#         web.URLSpec(r"/admin/refund/list.html", RefundListHandler, name="refund"),
#         web.URLSpec(r"/admin/refund/refund.html", OrderRefundHandler, name="order_refund"),
#         web.URLSpec(r"/admin/refund/express.html", RefundExpressHandler, name="refund_express"),
#         web.URLSpec(r"/admin/refund/agree.html", RefundAgreeHandler, name="refund_agree"),
#         web.URLSpec(r"/admin/refund/close.html", RefundCloseHandler, name="refund_close"),
#         web.URLSpec(r"/admin/refund/add_info.html", AppendRefundInfoHandler, name="refund_add_info"),
#         web.URLSpec(r"/admin/refund/view.html", RefundViewHandler, name="refund_view"),
#         web.URLSpec(pattern=r"/admin/refund/express/sign.html",
#                     handler=RefundExpressSignHandler,
#                     name="refund_express_sign"
#                     ),
#
#         web.URLSpec(r"/admin/supplier/list.html", SupplierListHandler, name="supplier"),
#         web.URLSpec(r"/admin/supplier/create.html", SupplierCreateHandler, name="supplier_create"),
#         web.URLSpec(r"/admin/supplier/edit.html", SupplierEditHandler, name="supplier_edit"),
#         web.URLSpec(r"/admin/supplier/view.html", SupplierViewHandler, name="supplier_view"),
#         web.URLSpec(r"/admin/supplier/check.html", SupplierCheckHandler, name="supplier_check"),
#
#         web.URLSpec(r"/upload/ueditor/upload.html", UEditorUploadHandler, name="ueditor_uploader"),
#         web.URLSpec(r"/upload/web/uploader.html", UploadImagesHandler, name="uploader"),
#         web.URLSpec(r"/select/content/list.html", ContentSelectListHandler, name="content_select"),
#
#         web.URLSpec(r"/admin/sync_cms.html", SyncCmsAdmin, name="sync_cms"),
#         web.URLSpec(r"/admin/kit/cms/banner.html", CMSBindBannerHandler, name="cms_bind_banner"),
#         web.URLSpec(r"/admin/kit/cms/product_contents.html", CMSBindContentHandler, name="cms_bind_product_contents"),
#         web.URLSpec(r"/admin/kit/cms/content/delete.html", DeleteCMSContentHandler, name="cms_del"),
#         web.URLSpec(r"/admin/kit/cms/content/updown.html", UpDownCMSContentHandler, name="cms_updown"),
#
#
#         web.URLSpec(r"/admin/sync_data.html", SyncDataHandler, name="sync_data")
#         ]
