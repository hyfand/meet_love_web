import os
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app, abort, jsonify
from app.models.share import Share, Comment
from app.models.user import Follow
from app.extensions import db
from flask_login import current_user, login_required
from app.form.share import ShareForm, ShareDeleteForm
from app.utils import random_filename, redirect_back, compress_image
from sqlalchemy import and_

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
            return redirect_back()
    return render_template("share/new_share.html", form=form)


@share_bp.route("/share_detail/<int:share_id>", methods=["GET", "POST"])
@share_bp.route("/share_detail/<int:share_id>/<int:page>", methods=["GET", "POST"])
def share_detail(share_id, page=1):
    comment_id = request.args.get("comment_id", type=int)  # 为了定位到评论处
    share = Share.query.get(share_id)
    per_page = current_app.config["DETAIL_SHARE_COMMENTS_PER_PAGE"]
    if comment_id:
        # 算出comment 在第几页 好跳转
        comment = Comment.query.get(comment_id)
        no = share.comments.filter_by(parent_id=None).order_by(Comment.time_stamp.desc()).all().index(comment) + 1
        page, more = divmod(no, per_page)
        if more:
            page += 1

    pagination = share.comments.filter_by(parent_id=None).order_by(Comment.time_stamp.desc()).paginate(page, per_page)
    comments = pagination.items


    return render_template("share/share_detail.html", share=share, comments=comments, pagination=pagination)


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


@share_bp.route("/praise_share", methods=["POST"])
@login_required
def praise_share():
    json = request.get_json()
    share_id = int(json.get("share_id"))
    op = json.get("op")
    share = Share.query.filter_by(id=share_id).first()
    if op == -1 and current_user in share.like_users:
        share.like_users.remove(current_user)
        share.author.receive_like_num -= 1
    elif op == 1 and current_user not in share.like_users:
        share.like_users.append(current_user)
        share.author.receive_like_num += 1
    db.session.commit()
    return jsonify({"status": "ok"}), 200


@share_bp.route("/concern_shares")
@share_bp.route("/concern_shares/<int:page>")
@login_required
def concern_shares(page=1):
    followed = db.session.query(Follow.followed_id).filter(Follow.follower_id == current_user.id).subquery()
    pagination = Share.query.filter(and_(Share.author_id.in_(followed), Share.author_id != current_user.id)).order_by(
        Share.publish_time.desc()).paginate(page, 10)
    shares = pagination.items
    return render_template("concerns.html", shares=shares, pagination=pagination)


@share_bp.route("/publish_comment", methods=["POST"])
@login_required
def publish_comment():
    content = request.form.get("comment_text")
    user_id = request.form.get("user_id", type=int)
    to_user_id = request.form.get("to_user_id", type=int)
    to_share_id = request.form.get("to_share_id", type=int)
    parent_id = request.form.get("parent_id", type=int)
    if content and user_id and to_user_id and to_share_id:
        comment = Comment(
            content=content,
            user_id=user_id,
            to_user_id=to_user_id,
            to_share_id=to_share_id,
            parent_id=parent_id
        )
        db.session.add(comment)
        db.session.commit()
        flash("😘评论成功")
    return redirect_back()


@share_bp.route("/receive_comments", methods=["GET"])
@share_bp.route("/receive_comments/<int:page>", methods=["GET"])
@login_required
def receive_comments(page=1):
    # 进来评论页面就将未读评论全部设置为已读
    unread_comments = Comment.query.filter_by(to_user_id=current_user.id, read=False).all()
    for comment in unread_comments:
        comment.read = True
    db.session.commit()

    pagination = Comment.query.filter_by(to_user_id=current_user.id).order_by(Comment.time_stamp.desc()).paginate(page, 10)
    comments = pagination.items
    return render_template("share/comments.html", comments=comments, pagination=pagination)
