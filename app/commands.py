import click
from app.extensions import db
from app.models.user import *
from app.models.share import *
import datetime
from faker import Faker
import random

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

    @app.cli.command()
    @click.option('--user', default=5, help='生成用户， 默认是5个')
    @click.option('--share', default=200, help='生成短文数量， 默认是200')
    def forge(user, share):

        db.drop_all()
        db.create_all()
        admin_register()

        fake = Faker(locale="zh_CN")
        click.echo('创建开发用的虚拟数据中...')
        for _ in range(user):
            user = User(
                user_name=fake.user_name(),
                password="123123123",
                real_name=fake.name(),
                nick_name=fake.name(),
                id_number=fake.ssn(min_age=18, max_age=18),
                sex=int(fake.boolean()),
                email=fake.email(),
                phone=fake.phone_number(),
                manifesto=fake.sentence(nb_words=10),
                register_time=fake.date_this_century(),
                confirm=True
            )
            db.session.add(user)
            db.session.commit()

        for _ in range(share):
            user_list = User.query.all()
            user = random.choice(user_list)
            share = Share(
                content=fake.paragraph(nb_sentences=6, variable_nb_sentences=True),
                author=user,
                publish_time=fake.date_time_between(start_date='-30d', end_date='-10d'),
                update_time=fake.date_time_between(start_date='-10d'),
                be_reported_num=random.randint(0, 20)
            )
            db.session.add(share)
            db.session.commit()
        click.echo('虚拟数据创建成功!')


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