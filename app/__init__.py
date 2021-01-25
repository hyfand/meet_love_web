from flask import Flask
from app.commands import register_app_command
from app.template_filter import register_template_filter
from config import Config
from app.extensions import login_manager
from app.extensions import db, ckeditor, moment, csrf
from flask_uploads import configure_uploads, patch_request_class
from app.uploads_set import potrait, photos

def create_app(config_name=None):
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

    configure_uploads(app, (photos, potrait))
    patch_request_class(app, 8 * 1024 * 1204)

    return app


def register_blueprint(app):
    from app.blueprint.user import user_bp
    from app.blueprint.main import main_bp
    from app.blueprint.share import share_bp
    app.register_blueprint(user_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(share_bp)
