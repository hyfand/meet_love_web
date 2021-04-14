from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_avatars import Avatars
from flask_dropzone import Dropzone
from flask_whooshee import Whooshee
from flask_admin import Admin
from flask_babelex import Babel
from flask_migrate import Migrate


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
dropzone = Dropzone()
whooshee = Whooshee()
babel = Babel()
migrate = Migrate()

from app.admin.admin_login import AdminIndexView
admin = Admin(name="遇爱管理后台", index_view=AdminIndexView(name="首页"), template_mode="bootstrap3", base_template="admin/my_base.html")
