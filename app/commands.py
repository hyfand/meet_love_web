import click
from app.extensions import db
from app.models.user import *
from app.models.share import *
import datetime

def register_app_command(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='删除数据库')
    def initdb(drop):
        if drop:
            click.confirm('这个操作会删除数据库, 你确定吗?')
            db.drop_all()
            click.echo('删除数据库成功!')
        db.create_all()
        admin_register()
        click.echo('初始化数据库!')


def admin_register():
    admin = User(
        user_name="admin",
        password="123123123",
        real_name="韩玉飞",
        nick_name="巴公战神",
        id_number="110110110110",
        sex=1,
        email="303498033@qq.com",
        phone="18001202682",
        manifesto="我是这个网站的老大",
        register_time=datetime.datetime.utcnow(),
        confirm=True
    )
    db.session.add(admin)
    db.session.commit()