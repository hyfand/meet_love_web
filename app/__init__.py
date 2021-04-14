from flask import Flask
from app.commands import register_app_command
from app.template_filter import register_template_filter
from config import Config
from app.extensions import login_manager
from app.extensions import db, ckeditor, moment, csrf, avatars, dropzone, whooshee, admin, babel, migrate
from flask_uploads import configure_uploads, patch_request_class
from app.uploads_set import photos


def create_app(config_name="development"):
    app = Flask(__name__)

    if config_name:
        config = Config.get(config_name)
        if config:
            app.config.from_object(config)
    else:
        app.config["SECRET_KEY"] = "test"
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    csrf.init_app(app)
    register_blueprint(app)
    register_app_command(app)
    register_template_filter(app)
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    login_manager.login_message_category = 'info'
    login_manager.login_message = '无权访问, 请登录。'
    avatars.init_app(app)
    dropzone.init_app(app)
    whooshee.init_app(app)
    admin.init_app(app)
    babel.init_app(app)
    migrate.init_app(app, db)

    configure_uploads(app, (photos, ))
    patch_request_class(app, 8 * 1024 * 1204)

    regiter_admin()

    return app


def register_blueprint(app):
    from app.blueprint.user import user_bp
    from app.blueprint.main import main_bp
    from app.blueprint.share import share_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(share_bp)


def regiter_admin():
    from app.admin.admin_login import AdminShareModelView, AdminCommentModelView, AdminUserModelView
    from app.models.share import Share, Comment
    from app.models.user import User
    admin.add_view(AdminUserModelView(User, db.session, name="用户", endpoint="admin_users"))
    admin.add_view(AdminShareModelView(Share, db.session, name="分享", endpoint="admin_shares"))
    admin.add_view(AdminCommentModelView(Comment, db.session, name="评论", endpoint="admin_comments"))
