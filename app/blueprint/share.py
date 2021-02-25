import os
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, abort
from app.models.share import Share
from app.extensions import db
from flask_login import current_user, login_required
from app.form.share import ShareForm, ShareDeleteForm
from app.utils import random_filename, redirect_back, compress_image

share_bp = Blueprint("share", __name__, url_prefix="/share")


@share_bp.route("/new_share", methods=["GET", "POST"])
@login_required
def new_share():
    form = ShareForm()
    if form.validate_on_submit():
        f = request.files.get('img')
        if f:
            new_filename = random_filename(f.filename)
            file = os.path.join(current_app.config['UPLOADED_PATH'], new_filename)
            f.save(file)
            compress_image(file)
        else:
            new_filename = ""
        new_share = Share(
            img=new_filename,
            content=form.content.data,
            author_id=current_user.id
        )
        try:
            db.session.add(new_share)
            db.session.commit()
            flash("发布成功!")
            return redirect(url_for("share.shares", user_id=current_user.id))
        except Exception:
            flash("发布失败 😱 请联系管理员！")
    return render_template("share/new_share.html", form=form)


@share_bp.route("/share_detail/<int:share_id>", methods=["GET", "POST"])
def share_detail(share_id):
    share = Share.query.get(share_id)
    return render_template("share/share_detail.html", share=share)


@share_bp.route("/shares/<int:user_id>")
@share_bp.route("/shares/<int:user_id>/<int:page>")
@login_required
def shares(user_id, page=1):
    form = ShareDeleteForm()
    # shares = Share.query.filter_by(author_id=user_id).order_by(Share.publish_time.desc()).all()
    pagination = Share.query.filter_by(author_id=user_id).order_by(Share.publish_time.desc()).paginate(page, 10)
    shares = pagination.items
    return render_template("share/shares.html", shares=shares, pagination=pagination, form=form)


@share_bp.route("/delete_share/<int:sid>", methods=["POST"])
@login_required
def delete_share(sid):
    form = ShareDeleteForm()
    if form.validate_on_submit():
        share = Share.query.filter_by(id=sid).first()
        db.session.delete(share)
        db.session.commit()
        if share.img:
            img_path = os.path.join(current_app.config['UPLOADED_PATH'], share.img)
            if os.path.exists(img_path):
                os.remove(img_path)
        flash("删除成功!")
    else:
        abort(400)
    return redirect_back()