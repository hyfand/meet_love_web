from app.models import db, Base
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime, Boolean, SmallInteger, Text
from datetime import datetime

class User(Base):
    __tablename__ = "tbl_user"
    id = Column(Integer, primary_key=True)
    user_name = Column(String(32), index=True, nullable=False)
    password_hash = Column(String(128))
    real_name = Column(String(32))
    id_number = Column(String(32))  # 身份证号码
    sex = Column(SmallInteger)  # 0 女 1 男 2 保密
    email = Column(String(254))
    phone = Column(String(30))
    manifesto = Column(Text)  # 个人宣言
    register_time = Column(DateTime, default=datetime.utcnow)
    confirm = Column(Boolean)

