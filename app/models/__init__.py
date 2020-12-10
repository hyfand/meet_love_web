from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Base = db.Model

from .user import *