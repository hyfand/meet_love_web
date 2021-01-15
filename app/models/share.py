from app.extensions import db
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime, Boolean, SmallInteger, Text
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import login_manager


class Share(db.Model):
    __tablename__ = "tbl_share"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), index=True, nullable=False)
    content = Column(String(5000))
    author_id = db.Column(db.Integer, db.ForeignKey("tbl_user.id"))
    author = db.relationship("User", backref=db.backref("share"))
    publish_time = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime, default=datetime.utcnow)
    be_reported_num = Column(db.Integer, default=0)  # 被举报次数