from app.extensions import db
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime, Boolean, SmallInteger, Text
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_avatars import Identicon

class User(db.Model, UserMixin):
    __tablename__ = "tbl_user"
    id = Column(Integer, primary_key=True)
    user_name = Column(String(32), index=True)
    password_hash = Column(String(128))
    real_name = Column(String(32))
    nick_name = Column(String(32))
    id_number = Column(String(32))  # 身份证号码
    sex = Column(SmallInteger)  # 0 女 1 男
    email = Column(String(254))
    phone = Column(String(30))
    manifesto = Column(Text)  # 个人宣言
    register_time = Column(DateTime, default=datetime.utcnow)
    confirm = Column(Boolean)

    avatar_s = db.Column(db.String(64))
    avatar_m = db.Column(db.String(64))
    avatar_l = db.Column(db.String(64))

    avatar_raw = db.Column(db.String(64))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generate_avatar()

    @property
    def password(self):
        return None

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_avatar(self):
        avatar = Identicon()
        filenames = avatar.generate(text=self.user_name)
        self.avatar_s = filenames[0]
        self.avatar_m = filenames[1]
        self.avatar_l = filenames[2]
        db.session.commit()
