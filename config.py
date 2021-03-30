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
    AVATARS_CROP_PREVIEW_SIZE = 100
    # AVATARS_CROP_INIT_SIZE = 100
    AVATARS_CROP_BASE_WIDTH = 350
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    DROPZONE_MAX_FILE_SIZE = 3
    DROPZONE_MAX_FILES = 3
    DROPZONE_ALLOWED_FILE_TYPE = "image"
    DROPZONE_DEFAULT_MESSAGE = "这里上传照片"
    DROPZONE_INVALID_FILE_TYPE = "只能传图片哦~"
    DROPZONE_MAX_FILE_EXCEED = "超过上传图片数量"
    DROPZONE_ENABLE_CSRF = True
    DROPZONE_SERVE_LOCAL = True

    WHOOSHEE_MIN_STRING_LEN = 1

    # 每页的数目
    SEARCH_RESULT_PER_PAGE = 20


class DevelopConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:303498@127.0.0.1/meet_love_test?charset=utf8mb4"
    # SQLALCHEMY_ECHO = True


class ProductConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:303498@127.0.0.1/meet_love?charset=utf8mb4"


Config = {
    "product": ProductConfig,
    "development": DevelopConfig
}
