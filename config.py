class BaseConfig:
    SECRET_KEY = "secret_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:303498@127.0.0.1/meet_love_test"


class ProductConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:303498@127.0.0.1/meet_love"