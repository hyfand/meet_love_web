from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

login_manager = LoginManager()
@login_manager.user_loader
def load_user(uid):
    from app.models.user import User
    user = User.query.get(int(uid))
    return user if user else None

db = SQLAlchemy()
