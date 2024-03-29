from app.extensions import db
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime, Text, Boolean
from datetime import datetime

share_like_table = db.Table("tbl_share_like",
                            db.Column("share_id", db.Integer, db.ForeignKey("tbl_share.id")),
                            db.Column("user_id", db.Integer, db.ForeignKey("tbl_user.id")))


class Share(db.Model):
    __tablename__ = "tbl_share"

    id = Column(Integer, primary_key=True)
    content = Column(Text(5000))
    img = Column(String(1000))
    author_id = db.Column(Integer, db.ForeignKey("tbl_user.id"))
    author = db.relationship("User", backref=db.backref("share"))
    publish_time = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime, default=datetime.utcnow)
    be_reported_num = Column(Integer, default=0)  # 被举报次数
    like_users = db.relationship("User", secondary=share_like_table, back_populates="like_shares")

    comments = db.relationship("Comment", backref="share", cascade="all", lazy="dynamic")

    def __repr__(self):
        return "%s ..." % self.content[:10]

    def like_users_count(self):
        return len(self.like_users)

    def comments_count(self):
        return self.comments.filter_by(parent_id=None).count()


class Comment(db.Model):
    __tablename__ = "tbl_comment"

    id = db.Column(Integer, primary_key=True)
    content = db.Column(String(200))
    time_stamp = Column(DateTime, default=datetime.utcnow)

    user_id = db.Column(Integer, db.ForeignKey("tbl_user.id"))  # 评论作者id
    user = db.relationship("User", foreign_keys=[user_id], back_populates="comments", lazy="joined")

    to_user_id = db.Column(Integer, db.ForeignKey("tbl_user.id"))  # 被评论作者id
    to_user = db.relationship("User", foreign_keys=[to_user_id], back_populates="receive_comments", lazy="joined")

    to_share_id = db.Column(Integer, db.ForeignKey("tbl_share.id"))  # 被评论的分享的id
    to_share = db.relationship("Share", foreign_keys=[to_share_id], back_populates="comments", lazy="joined")

    parent_id = db.Column(Integer, db.ForeignKey("tbl_comment.id"), nullable=True)  # 父评论id 支持多级评论
    sub_comments = db.relationship("Comment", foreign_keys=[parent_id], cascade="all", lazy="dynamic")

    read = db.Column(Boolean, default=False)
