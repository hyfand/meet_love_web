from flask import Flask
from app.commands import register_app_command
from config import Config
from app.extensions import login_manager

from app.extensions import db

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
    register_blueprint(app)
    register_app_command(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'
    login_manager.login_message = 'Access denied.'
    return app


def register_blueprint(app):
    from app.blueprint.user import user_bp
    app.register_blueprint(user_bp)
