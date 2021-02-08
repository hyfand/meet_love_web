from flask import Blueprint, render_template, current_app, send_from_directory, request, url_for
from flask_ckeditor import upload_success, upload_fail
from flask_ckeditor.utils import random_filename
from app.models.user import User
from app.models.share import Share
import os

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@main_bp.route("/<int:page>")
def index(page=1):
    # shares = Share.query.order_by(Share.publish_time.desc()).all()
    pagination = Share.query.order_by(Share.publish_time.desc()).paginate(page, 10)
    shares = pagination.items
    return render_template("index.html", shares=shares, pagination=pagination)


@main_bp.route("/avatars/<path:filename>")
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)


@main_bp.route("/files/<filename>")
def uploaded_files(filename):
    return send_from_directory(current_app.config['UPLOADED_PATH'], filename)


@main_bp.route("/upload", methods=["POST"])
def upload():
    f = request.files.get('upload')
    extension = f.filename.split('.')[-1].lower()
    if extension not in ['jpg', 'gif', 'png', 'jpeg']:
        return upload_fail(message='Image only!')
    new_filename = random_filename(f.filename)
    f.save(os.path.join(current_app.config['UPLOADED_PATH'], new_filename))
    url = url_for('main.uploaded_files', filename=new_filename)
    return upload_success(url=url)
