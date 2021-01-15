class BaseConfig:
    SECRET_KEY = "secret_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_PKG_TYPE = "standard"
    CKEDITOR_FILE_UPLOADER = "main.upload"
    CKEDITOR_EXTRA_PLUGINS = ["filebrowser"]


class DevelopConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:303498@127.0.0.1/meet_love_test"
    # SQLALCHEMY_ECHO = True


class ProductConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:303498@127.0.0.1/meet_love"


Config = {
    "product": ProductConfig,
    "development": DevelopConfig
}
