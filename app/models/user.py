from app.models import db, Base
from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime, BOOLEAN

class User(Base):
    __tablename__ = "tbl_user"
    id = Column(Integer, primary_key=True)
    name = Column(String(32), index=True, nullable=False)

