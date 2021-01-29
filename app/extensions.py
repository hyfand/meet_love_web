from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_avatars import Avatars

login_manager = LoginManager()
@login_manager.user_loader
def load_user(uid):
    from app.models.user import User
    user = User.query.get(int(uid))
    return user if user else None

db = SQLAlchemy()
ckeditor = CKEditor()
moment = Moment()
csrf = CSRFProtect()
avatars = Avatars()