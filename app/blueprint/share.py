from flask import Blueprint, render_template, flash, redirect, url_for
from app.models.share import Share
from app.extensions import db
from flask_login import current_user, login_required
from app.form.share import ShareForm

share_bp = Blueprint("share", __name__, url_prefix="/share")


@share_bp.route("/new_share", methods=["GET", "POST"])
@login_required
def new_share():
    form = ShareForm()
    if form.validate_on_submit():
        new_share = Share(
            content=form.content.data,
            author_id=current_user.id
        )
        print(form.content.data)
        try:
            db.session.add(new_share)
            db.session.commit()
            flash("发布成功!")
            return redirect(url_for("share.share_detail", share_id=new_share.id))
        except Exception:
            flash("发布失败 😱 请联系管理员！")
    return render_template("share/new_share.html", form=form)


@share_bp.route("/share_detail/<int:share_id>", methods=["GET", "POST"])
def share_detail(share_id):
    share = Share.query.get(share_id)
    return render_template("share/share_detail.html", share=share)


@share_bp.route("/shares/<int:user_id>")
@login_required
def shares(user_id):
    shares = Share.query.filter_by(author_id=user_id).order_by(Share.publish_time.desc()).all()
    print(shares)
    return render_template("share/shares.html", shares=shares)