# coding:utf-8
"""同步cms

Revision ID: 83226c7c1359
Revises: a4146bdf2d7f
Create Date: 2016-05-16 10:42:40.613000

"""

# revision identifiers, used by Alembic.
revision = '83226c7c1359'
down_revision = 'a4146bdf2d7f'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("""
      alter table `order_cancels` drop column `cancel_no`
    """)

    # 同步CMS
    op.execute(
        """
        CREATE TABLE `cms_content` (
           `id` integer NOT NULL AUTO_INCREMENT,
           `created_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
           `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
           `image` varchar(200) NOT NULL DEFAULT '',
           `custom_image_size` varchar(10) NOT NULL DEFAULT '410*236',
           `target` varchar(30) NOT NULL DEFAULT '',
           `type` integer  NOT NULL,
           `ordering` tinyint NOT NULL DEFAULT '0',
           PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """
    )

    # express运单表添加status状态字段
    op.execute("""
      alter table `express` add column `status` tinyint NOT NULL DEFAULT '0'
    """)


def downgrade():
    pass