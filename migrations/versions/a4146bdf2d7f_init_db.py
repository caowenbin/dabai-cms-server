# coding: utf-8
"""初始化表

Revision ID: a4146bdf2d7f
Revises: 
Create Date: 2016-04-08 13:04:56.387851

"""

# revision identifiers, used by Alembic.
revision = 'a4146bdf2d7f'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    # 管理员表
    op.execute(
            """
            CREATE TABLE `administrators` (
               `id` smallint NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `fullname` varchar(20) NOT NULL DEFAULT '',
               `password` varchar(40) NOT NULL DEFAULT '',
               `email` varchar(30) NOT NULL DEFAULT '' UNIQUE,
               `confirmed` tinyint NOT NULL DEFAULT '0',
               `administer` tinyint NOT NULL DEFAULT '0',
               `validity` tinyint NOT NULL DEFAULT '1',
               `last_login_time` timestamp NULL DEFAULT NULL,
               `last_login_ip` varchar(16) NOT NULL DEFAULT '',
               PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )
    # 密码为admin.cicaero.com
    op.execute(
            """
            INSERT INTO `administrators` VALUES ('1', '2016-04-11 09:52:01', '2016-04-11 09:53:51', 'administrator', '85f1e4ea60d03e19451f7486416ec7eaf9b16b20', 'admin@cicaero.com', '1', '1', '1', null, '');
            """
    )
    # 可配送地区表
    op.execute(
            """
            CREATE TABLE `cover_areas` (
               `id` smallint NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `province_code` varchar(10) NOT NULL DEFAULT '',
               `province_name` varchar(20) NOT NULL DEFAULT '',
               `city_code` varchar(10) NOT NULL DEFAULT '',
               `city_name` varchar(20) NOT NULL DEFAULT '',
               `area_code` varchar(10) NOT NULL DEFAULT '' UNIQUE,
               `area_name` varchar(20) NOT NULL DEFAULT '',
               PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 分类表
    op.execute(
            """
            CREATE TABLE `categories` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `parent_id` integer NOT NULL DEFAULT 0,
               `name` varchar(20) NOT NULL DEFAULT '',
               `validity` tinyint NOT NULL DEFAULT '1',
               PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 渠道表
    op.execute(
            """
            CREATE TABLE `channels` (
               `id` smallint NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `channel_code` varchar(15) NOT NULL DEFAULT '' UNIQUE,
               `name` varchar(20) NOT NULL DEFAULT '',
               `remarks` varchar(30) NOT NULL DEFAULT '',
               `secret_key` varchar(50) NOT NULL DEFAULT '',
               `validity` tinyint NOT NULL DEFAULT '1',
               PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 品牌表
    op.execute(
            """
            CREATE TABLE `brands` (
               `id` smallint NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `name` varchar(20) NOT NULL DEFAULT '' UNIQUE,
               PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 供应商表
    op.execute(
            """
            CREATE TABLE `suppliers` (
               `id` smallint NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `fullname` varchar(30) NOT NULL DEFAULT '',
               `login_name` varchar(30) NOT NULL DEFAULT '' UNIQUE,
               `password` varchar(40) NOT NULL DEFAULT '',
               `contact_name` varchar(20) NOT NULL DEFAULT '',
               `contact_phone` varchar(11) NOT NULL DEFAULT '',
               `validity` tinyint NOT NULL DEFAULT '1',
               `last_login_time` timestamp NULL DEFAULT NULL,
               `last_login_ip` varchar(16) NOT NULL DEFAULT '',
               `operator` varchar(20) NOT NULL DEFAULT '',
               PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 焦点图表
    op.execute(
            """
            CREATE TABLE `banners` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `banner_code` varchar(15) NOT NULL DEFAULT '' UNIQUE,
               `name` varchar(30) NOT NULL DEFAULT '',
               `banner_type` tinyint NOT NULL DEFAULT '0',
               `target` varchar(50) NOT NULL DEFAULT '',
               `image` varchar(200) NOT NULL DEFAULT '',
               `remark` varchar(30) NOT NULL DEFAULT '',
               `validity` tinyint NOT NULL DEFAULT '1',
               PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 货品属性表
    op.execute(
            """
            CREATE TABLE `attributes` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `category_id` integer NOT NULL DEFAULT '0',
               `name` varchar(20) NOT NULL DEFAULT '',
               `ordering` tinyint NOT NULL DEFAULT '1',
               `is_del` tinyint NOT NULL DEFAULT '0',
               PRIMARY KEY (`id`),
               FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 属性选项值表
    op.execute(
            """
            CREATE TABLE `attribute_items` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `attr_id` integer NOT NULL DEFAULT '0',
               `attr_value` varchar(20) NOT NULL DEFAULT '',
               `is_del` tinyint NOT NULL DEFAULT '0',
               `ordering` tinyint NOT NULL DEFAULT '1',
               PRIMARY KEY (`id`),
               FOREIGN KEY (`attr_id`) REFERENCES `attributes` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 角标表
    op.execute(
            """
            CREATE TABLE `corner_marks` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `image` varchar(200) NOT NULL DEFAULT '',
               `group_name` varchar(30) NOT NULL DEFAULT '',
               PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 货品表
    op.execute(
            """
            CREATE TABLE `products` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `first_category` integer NOT NULL DEFAULT '0',
               `second_category` integer NOT NULL DEFAULT '0',
               `third_category` integer NOT NULL DEFAULT '0',
               `spu` varchar(20) NOT NULL DEFAULT '' UNIQUE,
               `full_name` varchar(100) NOT NULL DEFAULT '',
               `title` varchar(50) NOT NULL DEFAULT '',
               `short_name` varchar(20) NOT NULL DEFAULT '',
               `supplier_id` smallint NOT NULL,
               `brand_name` varchar(20) NOT NULL DEFAULT '',
               `limits` smallint NOT NULL DEFAULT '0',
               `sales_volume` integer NOT NULL DEFAULT '0',
               `product_type` tinyint NOT NULL DEFAULT '0',
               `validity` tinyint NOT NULL DEFAULT '1',
               `is_del` tinyint NOT NULL DEFAULT '0',
               `image_text` text NOT NULL,
               `image_text_pad` text NOT NULL,
               `market_text` varchar(150) NOT NULL DEFAULT '',
               `about_text` varchar(150) NOT NULL DEFAULT '',
               `out_way` tinyint NOT NULL DEFAULT '0',
               PRIMARY KEY (`id`),
               FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 货品图片表
    op.execute(
            """
            CREATE TABLE `product_pictures` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `product_id` integer NOT NULL,
               `label` tinyint NOT NULL DEFAULT '0',
               `image` varchar(200) NOT NULL DEFAULT '',
               `ordering` tinyint NOT NULL DEFAULT '0',
               `is_del` tinyint NOT NULL DEFAULT '0',
               PRIMARY KEY (`id`),
               FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 商品表(sku)
    op.execute(
            """
            CREATE TABLE `goods` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `product_id` integer NOT NULL,
               `sku` varchar(30) NOT NULL DEFAULT '' UNIQUE,
               `price` integer NOT NULL DEFAULT '0',
               `stock` smallint NOT NULL DEFAULT '0',
               `is_default` tinyint NOT NULL DEFAULT '0',
               `is_del` tinyint NOT NULL DEFAULT '0',
               `properties` varchar(200) NOT NULL DEFAULT '',
               `property_names` varchar(200) NOT NULL DEFAULT '',
               PRIMARY KEY (`id`),
               FOREIGN KEY (`product_id`) REFERENCES `products` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 频道表
    op.execute(
            """
            CREATE TABLE `groups` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `group_code` varchar(20) NOT NULL DEFAULT '' UNIQUE,
               `name` varchar(20) NOT NULL DEFAULT '',
               `is_home` tinyint NOT NULL DEFAULT '0',
               `validity` tinyint NOT NULL DEFAULT '1',
               `ordering` tinyint NOT NULL DEFAULT '0',
               PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 频道与渠道关联表
    op.execute(
            """
            CREATE TABLE `group_channels` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `group_id` integer NOT NULL,
               `channel_code` varchar(15) NOT NULL DEFAULT '',
               PRIMARY KEY (`id`),
               FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 频道模板表
    op.execute(
            """
            CREATE TABLE `group_templates` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `group_id` integer NOT NULL,
               `column_name` varchar(20) NOT NULL DEFAULT '',
               `is_show_name` tinyint NOT NULL DEFAULT '0',
               `column_icon` varchar(200) NOT NULL DEFAULT '',
               `is_show_icon` tinyint NOT NULL DEFAULT '0',
               `template_code` varchar(10) NOT NULL DEFAULT '',
               `ordering` tinyint NOT NULL DEFAULT '0',
               PRIMARY KEY (`id`),
               FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 模板内容
    op.execute(
            """
            CREATE TABLE `template_contents` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `group_id` integer NOT NULL,
               `group_template_id` integer NOT NULL,
               `content_type` tinyint NOT NULL DEFAULT '0',
               `custom_title` varchar(50) NOT NULL DEFAULT '',
               `remark` varchar(30) NOT NULL DEFAULT '',
               `custom_image` varchar(200) NOT NULL DEFAULT '',
               `custom_image_size` varchar(10) NOT NULL DEFAULT '448*338',
               `content_code` varchar(30) NOT NULL DEFAULT '',
               `corner_mark_image` varchar(200) NOT NULL DEFAULT '',
               `ordering` tinyint NOT NULL DEFAULT '0',
               `start_time` timestamp NULL,
               `end_time` timestamp NULL,
               PRIMARY KEY (`id`),
               FOREIGN KEY (`group_id`) REFERENCES `groups` (`id`),
               FOREIGN KEY (`group_template_id`) REFERENCES `group_templates` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 订单表
    op.execute(
            """
            CREATE TABLE `orders` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `order_no` varchar(25) NOT NULL DEFAULT '' UNIQUE,
               `pay_channel_code` varchar(15) NOT NULL DEFAULT '',
               `pay_type` varchar(15) NOT NULL DEFAULT '',
               `trade_no` varchar(30) NULL UNIQUE,
               `pay_time` timestamp NULL,
               `order_status` tinyint NOT NULL DEFAULT '0',
               `price` integer NOT NULL DEFAULT '0',
               `post_fee` integer NOT NULL DEFAULT '0',
               `goods_total_price` integer NOT NULL DEFAULT '0',
               `buyer_code` varchar(30) NOT NULL DEFAULT '',
               `buyer_phone` varchar(11) NOT NULL DEFAULT '',
               `channel_code` varchar(15) NOT NULL DEFAULT '',
               `supplier_id` smallint NOT NULL DEFAULT '0',
               `receiver` varchar(20) NOT NULL DEFAULT '',
               `receiver_province` varchar(15) NOT NULL DEFAULT '',
               `receiver_city` varchar(15) NOT NULL DEFAULT '',
               `receiver_area` varchar(15) NOT NULL DEFAULT '',
               `receiver_address` varchar(60) NOT NULL DEFAULT '',
               `receiver_phone` varchar(11) NOT NULL DEFAULT '',
               `make_invoice` tinyint NOT NULL DEFAULT '0',
               PRIMARY KEY (`id`),
               INDEX  (`created_time`),
               INDEX  (`receiver`),
               INDEX  (`receiver_phone`),
               INDEX  (`order_status`),
               INDEX  (`buyer_phone`),
               INDEX  (`channel_code`),
               INDEX  (`supplier_id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 订单发票表
    op.execute(
            """
            CREATE TABLE `order_invoices` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `order_id` integer NOT NULL DEFAULT '0',
               `invoice_type` tinyint NOT NULL DEFAULT '0',
               `invoice_content` tinyint NOT NULL DEFAULT '1',
               `invoice_title` tinyint NOT NULL DEFAULT '0',
               `company_name` varchar(30) NOT NULL DEFAULT '',
               `gateman_phone` varchar(11) NOT NULL DEFAULT '',
               `gateman_email` varchar(30) NOT NULL DEFAULT '',
               PRIMARY KEY (`id`),
               FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 订单商品表
    op.execute(
            """
            CREATE TABLE `order_details` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `order_id` integer NOT NULL DEFAULT '0',
               `first_category_name` varchar(20) NOT NULL DEFAULT '',
               `second_category_name` varchar(20) NOT NULL DEFAULT '',
               `third_category_name` varchar(20) NOT NULL DEFAULT '',
               `product_spu` varchar(20) NOT NULL DEFAULT '',
               `brand_name` varchar(20) NOT NULL DEFAULT '',
               `product_type` tinyint NOT NULL DEFAULT '0',
               `goods_sku` varchar(20) NOT NULL DEFAULT '',
               `goods_image` varchar(200) NOT NULL DEFAULT '',
               `goods_specs` varchar(100) NOT NULL DEFAULT '',
               `goods_fullname` varchar(30) NOT NULL DEFAULT '',
               `goods_title` varchar(30) NOT NULL DEFAULT '',
               `quantity` SMALLINT NOT NULL DEFAULT '0',
               `price` integer NOT NULL DEFAULT '0',
               PRIMARY KEY (`id`, `order_id`, `goods_sku`),
               FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 退款表
    op.execute(
            """
            CREATE TABLE `refunds` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `order_id` integer NOT NULL DEFAULT '0',
               `order_no` varchar(20) NOT NULL DEFAULT '',
               `order_goods_id` integer NOT NULL DEFAULT '0',
               `pay_trade_no` varchar(30) NOT NULL DEFAULT '',
               `refund_no` varchar(20) NOT NULL DEFAULT '' UNIQUE,
               `refund_trade_no` varchar(30) NOT NULL DEFAULT '',
               `refund_type` varchar(10) NOT NULL DEFAULT '',
               `refund_reason_code` varchar(10) NOT NULL DEFAULT '',
               `remark` varchar(50) NOT NULL DEFAULT '',
               `refund_status` tinyint NOT NULL DEFAULT '0',
               `refund_fee` integer NOT NULL DEFAULT '0',
               `return_invoice` tinyint NOT NULL DEFAULT '0',
               `receiver` varchar(20) NOT NULL DEFAULT '',
               `receiver_phone` varchar(11) NOT NULL DEFAULT '',
               `receiver_address` varchar(50) NOT NULL DEFAULT '',
               `supplier_id` smallint NOT NULL DEFAULT '0',
               `channel_id` smallint NOT NULL DEFAULT '0',
               `operator` varchar(20) NOT NULL DEFAULT '',
               PRIMARY KEY (`id`),
               FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
               FOREIGN KEY (`order_goods_id`) REFERENCES `order_details` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 退款凭证表
    op.execute(
            """
            CREATE TABLE `refund_evidences` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `refund_id` integer NOT NULL DEFAULT '0',
               `evidence_image` varchar(200) NOT NULL DEFAULT '',
               PRIMARY KEY (`id`),
               FOREIGN KEY (`refund_id`) REFERENCES `refunds` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 订单取消表
    op.execute(
            """
            CREATE TABLE `order_cancels` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `order_id` integer NOT NULL,
               `cancel_no` varchar(20) UNIQUE,
               `cancel_code` varchar(10) NOT NULL DEFAULT '',
               `cancel_remark` varchar(100) NOT NULL DEFAULT '',
               `operator` varchar(20) NOT NULL DEFAULT '',
               PRIMARY KEY (`id`),
               FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 快递单号表
    op.execute(
            """
            CREATE TABLE `express` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `record_type` tinyint NOT NULL DEFAULT '0',
               `record_value` varchar(20) NOT NULL DEFAULT '',
               `track_number` varchar(20) NOT NULL DEFAULT '' UNIQUE,
               `express_code` varchar(20) NOT NULL DEFAULT '',
               PRIMARY KEY (`id`),
               INDEX  (`record_type`, `record_value`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 用户表
    op.execute(
            """
            CREATE TABLE `users` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `user_number` varchar(30) NOT NULL DEFAULT '' UNIQUE,
               `nickname` varchar(20) NOT NULL DEFAULT '',
               `mobile` varchar(11) NOT NULL DEFAULT '' UNIQUE,
               `email` varchar(30) NOT NULL DEFAULT '' UNIQUE,
               `pwd` varchar(40) NOT NULL DEFAULT '',
               `sex` varchar(2) NOT NULL DEFAULT '',
               `login_count` smallint NOT NULL DEFAULT '0',
               `last_login_time` timestamp NULL,
               `last_login_ip` varchar(20) NOT NULL DEFAULT '',
               `last_login_channel` tinyint NULL,
               `birth_date` timestamp NULL,
               PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

    # 第三方用户表
    op.execute(
            """
            CREATE TABLE `auth_users` (
               `id` integer NOT NULL AUTO_INCREMENT,
               `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
               `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
               `user_id` integer NOT NULL,
               `auth_user_name` varchar(30) NOT NULL DEFAULT '',
               `auth_channel` tinyint NOT NULL DEFAULT '0',
               PRIMARY KEY (`id`),
               FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            """
    )

def downgrade():
    pass
