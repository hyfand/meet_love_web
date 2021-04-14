from flask import Blueprint, render_template, current_app, send_from_directory, request, url_for, flash
from flask_login import current_user
from flask_ckeditor import upload_success, upload_fail
from flask_ckeditor.utils import random_filename
from app.models.user import User
from app.models.share import Share
import os
from app.utils import redirect_back
from sqlalchemy.sql.expression import func

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
    return send_from_directory(current_app.config["AVATARS_SAVE_PATH"], filename)


@main_bp.route("/files/<filename>")
def uploaded_files(filename):
    return send_from_directory(current_app.config["UPLOADED_PATH"], filename)


@main_bp.route("/upload", methods=["POST"])
def upload():
    f = request.files.get("upload")
    extension = f.filename.split(".")[-1].lower()
    if extension not in ["jpg", "gif", "png", "jpeg"]:
        return upload_fail(message="Image only!")
    new_filename = random_filename(f.filename)
    f.save(os.path.join(current_app.config["UPLOADED_PATH"], new_filename))
    url = url_for("main.uploaded_files", filename=new_filename)
    return upload_success(url=url)


@main_bp.route("/person/<int:user_id>")
@main_bp.route("/person/<int:user_id>/<int:page>")
def person(user_id, page=1):
    user = User.query.filter_by(id=user_id).first()
    pagination = Share.query.filter_by(author_id=user_id).order_by(Share.publish_time.desc()).paginate(page, 10)
    shares = pagination.items
    return render_template("/person_page.html", shares=shares, pagination=pagination, user=user)


@main_bp.route("/search")
def search():
    q = request.args.get("q")
    if q == "":
        flash("搜索字段不能为空")
        return redirect_back()
    category = request.args.get("category", "user")
    page = request.args.get("page", 1, type=int)
    per_page = current_app.config["SEARCH_RESULT_PER_PAGE"]
    if category == "user":
        pagination = User.query.whooshee_search(q).paginate(page, per_page)
    result = pagination.items

    return render_template("search_result.html", result=result, pagination=pagination, q=q, category=category)


@main_bp.route("/explore")
def explore():
    shares = Share.query.order_by(func.random()).limit(5)
    return render_template("explore.html", shares=shares)


@main_bp.route("/about_site")
def about_site():
    return render_template("about_site.html")