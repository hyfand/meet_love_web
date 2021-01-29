import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = "secret_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CKEDITOR_SERVE_LOCAL = True
    # CKEDITOR_PKG_TYPE = "standard"
    CKEDITOR_PKG_TYPE = "basic"
    CKEDITOR_FILE_UPLOADER = "main.upload"
    CKEDITOR_EXTRA_PLUGINS = ["filebrowser"]
    CKEDITOR_ENABLE_CSRF = True
    UPLOADED_PATH = os.path.join(base_dir, "uploads")  # ckeditor 上传
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir, "uploads")  # 照片

    AVATARS_SAVE_PATH = os.path.join(base_dir, "avatars")  # 头像
    AVATARS_SIZE_TUPLE = (30, 100, 300)

class DevelopConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:303498@127.0.0.1/meet_love_test"
    SQLALCHEMY_ECHO = True


class ProductConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:303498@127.0.0.1/meet_love"


Config = {
    "product": ProductConfig,
    "development": DevelopConfig
}
