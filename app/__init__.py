from flask import Flask
from app.models import db

def create_app(config_obj=None):
    app = Flask(__name__)
    if config_obj:
        app.config.from_object(config_obj)
    else:
        app.config["SECRET_KEY"] = "test"
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    register_blueprint(app)
    return app


def register_blueprint(app):
    from app.blueprint.user import user_bp
    app.register_blueprint(user_bp)
