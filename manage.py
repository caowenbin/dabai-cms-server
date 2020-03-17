# coding:utf-8
import os

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from application import Application
from extends import db

__author__ = 'bin wen'

env = os.environ.get('DB_PROJECT_ENV', 'default')  # 主要用于配置对应的配置
service = os.environ.get('DB_PROJECT_SERVICE', 'all')  # 主要用于是admin还是api服务

app = Application(
    service=service,
    env=env
)
manager = Manager(app)
migrate = Migrate(app=app, db=db)


def make_shell_context():
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
