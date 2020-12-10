import click
from app.models import db

def register_app_command(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='删除数据库')
    def initdb(drop):
        if drop:
            click.confirm('这个操作会删除数据库, 你确定吗?')
            db.drop_all()
            click.echo('删除数据库成功!')
        db.create_all()
        click.echo('初始化数据库!')