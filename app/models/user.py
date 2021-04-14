from app.extensions import db, whooshee
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime, Boolean, SmallInteger, Text
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_avatars import Identicon
from app.models.share import share_like_table, Comment

class Follow(db.Model):
    __tablename__ = "tbl_follow"

    follower_id = db.Column(db.Integer, db.ForeignKey("tbl_user.id"), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey("tbl_user.id"), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    follower = db.relationship("User", foreign_keys=[follower_id], back_populates="following", lazy="joined")
    followed = db.relationship("User", foreign_keys=[followed_id], back_populates="followers", lazy="joined")

@whooshee.register_model("user_name", "nick_name")
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

    like_shares = db.relationship("Share", secondary=share_like_table, back_populates="like_users")

    following = db.relationship("Follow", foreign_keys=[Follow.follower_id], back_populates="follower", lazy="dynamic", cascade="all")
    followers = db.relationship("Follow", foreign_keys=[Follow.followed_id], back_populates="followed", lazy="dynamic",
                                cascade="all")

    comments = db.relationship("Comment", foreign_keys=[Comment.user_id], back_populates="user", lazy="dynamic", cascade="all")
    receive_comments = db.relationship("Comment", foreign_keys=[Comment.to_user_id], back_populates="to_user", lazy="dynamic", cascade="all")

    receive_like_num = db.Column(Integer, default=0)
    admin = db.Column(Boolean, default=False)

    def __repr__(self):
        return "%s %s" % (self.user_name, self.nick_name)

    def unread_receive_comments_count(self):
        return self.receive_comments.filter_by(read=False).count()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.generate_avatar()
        self.follow(self)

    @property
    def is_admin(self):
        if self.user_name == "admin" or self.admin:
            return True
        return False

    # 登录了并且是管理员
    @property
    def authenticated_and_admin(self):
        return self.is_authenticated() and self.is_admin

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

    def follow(self, user):
        if not self.is_following(user):
            follow = Follow(follower=self, followed=user)
            db.session.add(follow)
            db.session.commit()
            return True
        return False

    def unfollow(self, user):
        follow = self.following.filter_by(followed_id=user.id).first()
        if follow:
            db.session.delete(follow)
            db.session.commit()
            return True
        return False

    def is_following(self, user):
        if user.id is None:
            return False
        return self.following.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    # 所有用户关注自己
    def follow_self_all(self):
        for user in User.query.all():
            user.follow(user)