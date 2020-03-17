# coding:utf-8
"""修改供应商\订单\退款\轮播图

Revision ID: 95a5e6ba5576
Revises: 83226c7c1359
Create Date: 2016-05-19 17:58:45.904519

"""

# revision identifiers, used by Alembic.
revision = '95a5e6ba5576'
down_revision = '83226c7c1359'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute(
                """
                ALTER TABLE `suppliers` CHANGE `contact_phone` `contact_phone` VARCHAR(20)  CHARACTER SET utf8  COLLATE utf8_general_ci  NOT NULL  DEFAULT '';
                ALTER TABLE `suppliers` ADD `short_name` VARCHAR(20)  CHARACTER SET utf8  COLLATE utf8_general_ci  NULL  DEFAULT '';
                ALTER TABLE `banners` CHANGE `target` `target` VARCHAR(200)  CHARACTER SET utf8  COLLATE utf8_general_ci  NOT NULL  DEFAULT '';

                """
    )

    op.execute(
                """
                ALTER TABLE `refunds` CHANGE `remark` `remark` VARCHAR(500)  CHARACTER SET utf8  COLLATE utf8_general_ci  NOT NULL  DEFAULT '';
                ALTER TABLE `orders` ADD `remark` VARCHAR(100)  CHARACTER SET utf8  COLLATE utf8_general_ci  NULL  DEFAULT '';
                ALTER TABLE `refunds` CHANGE `channel_id` `channel_code` VARCHAR(15)  CHARACTER SET utf8  COLLATE utf8_general_ci  NOT NULL  DEFAULT '';
                """
    )

    op.execute("""alter table `product_pictures` drop column `is_del`;""")


def downgrade():
    pass
