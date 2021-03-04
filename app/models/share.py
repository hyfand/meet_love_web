from app.extensions import db
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime, Boolean, SmallInteger, Text
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import login_manager


share_like_table = db.Table("share_like_table",
                            db.Column("share_id", db.Integer, db.ForeignKey("tbl_share.id")),
                            db.Column("user_id", db.Integer, db.ForeignKey("tbl_user.id")))


class Share(db.Model):
    __tablename__ = "tbl_share"
    id = Column(Integer, primary_key=True)
    content = Column(String(5000))
    img = Column(String(1000))
    author_id = db.Column(db.Integer, db.ForeignKey("tbl_user.id"))
    author = db.relationship("User", backref=db.backref("share"))
    publish_time = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime, default=datetime.utcnow)
    be_reported_num = Column(db.Integer, default=0)  # 被举报次数
    like_users = db.relationship("User", secondary=share_like_table, back_populates="like_shares")

    def like_users_count(self):
        return len(self.like_users)


