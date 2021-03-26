import os
from PIL import Image
from flask import Blueprint, render_template, flash, redirect, url_for, current_app, request, jsonify
from app.form.user import UserRegisterForm, UserLoginForm, UserChangeInfoForm, UserChangePasswordForm, UserAvatarForm, CropAvatarForm
from app.models.user import *
from app.extensions import db, avatars
from flask_login import login_user, logout_user, current_user, login_required
from app.utils import redirect_back, random_filename
from app.uploads_set import photos


user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.route("/register", methods=["GET", "POST"])
def register():
    form = UserRegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(user_name=form.user_name.data).first():
            flash("账号名已存在!")
        elif User.query.filter_by(email=form.email.data).first():
            flash("邮箱已存在!")
        elif User.query.filter_by(phone=form.phone.data).first():
            flash("手机号已经存在!")
        else:
            user = User(
                user_name=form.user_name.data,
                nick_name=form.nick_name.data,
                # real_name=form.real_name.data,
                # id_number=form.id_number.data,
                sex=form.sex.data,
                password=form.password.data,
                email=form.email.data,
                phone=form.phone.data,
                manifesto=form.manifesto.data
            )
            db.session.add(user)
            db.session.commit()
            flash("注册成功, 请登录!")
            return redirect(url_for('.login'))
    return render_template("user/user_register.html", form=form)


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = UserLoginForm()
    if form.validate_on_submit():
        user_name = form.user_name.data
        password = form.password.data
        remember = form.remember.data
        user = User.query.filter_by(user_name=user_name).first()
        if user:
            if user.check_password(password):
                login_user(user, remember)
                flash("欢迎登录!", "info")
                return redirect_back()
            flash("密码错误!", "warning")
        else:
            flash("用户不存在!", "warning")
    return render_template("user/user_login.html", form=form)


@user_bp.route("/logout")
def logout():
    logout_user()
    flash("退出成功", "info")
    return redirect_back()


@user_bp.route("/user_info")
@login_required
def user_info():
    return render_template("user/user_info.html")


@user_bp.route("/user_avatar_modify", methods=["GET", "POST"])
@login_required
def user_avatar_modify():
    avatar_form = UserAvatarForm()
    crop_form = CropAvatarForm()
    return render_template("user/user_avatar_modify.html", avatar_form=avatar_form, crop_form=crop_form)


@user_bp.route("/user_avatar_upload", methods=["POST"])
@login_required
def user_avatar_upload():
    form = UserAvatarForm()
    if form.validate_on_submit():
        image = form.image.data
        raw_img = Image.open(image)
        if raw_img.size[0] > 300:
            raw_img = avatars.resize_avatar(raw_img, 300)
        filename = avatars.save_avatar(raw_img)
        current_user.avatar_raw = filename
        db.session.commit()
        flash("头像上传成功, 请剪切哟")
    else:
        flash("头像上传失败~" + form.errors["image"][0])
    return redirect(url_for(".user_avatar_modify"))


@user_bp.route("/user_avatar_crop", methods=["POST"])
@login_required
def user_avatar_crop():
    form = CropAvatarForm()
    if form.validate_on_submit():
        x = form.x.data
        y = form.y.data
        w = form.w.data
        h = form.h.data
        filenames = avatars.crop_avatar(current_user.avatar_raw, x, y, w, h)
        current_user.avatar_s = filenames[0]
        current_user.avatar_m = filenames[1]
        current_user.avatar_l = filenames[2]
        db.session.commit()
        flash("头像上传成功！")

    return redirect(url_for(".user_avatar_modify"))

@user_bp.route("/user_info_modify", methods=["GET", "POST"])
@login_required
def user_info_modify():
    form = UserChangeInfoForm()
    if form.is_submitted():
        if form.validate():
            current_user.nick_name = form.nick_name.data
            current_user.email = form.email.data
            current_user.phone = form.phone.data
            current_user.manifesto = form.manifesto.data
            try:
                db.session.commit()
                flash("嘿嘿 ❤ 信息修改成功！")
            except Exception:
                flash("保存失败 😱 请联系管理员！")
                db.session.rollback()
            return redirect(url_for("user.user_info"))
        else:
            flash("哎呀 😱 请检查输入是否正确！")
            return render_template("user/user_info_modify.html", form=form)
    form.nick_name.data = current_user.nick_name
    form.email.data = current_user.email
    form.phone.data = current_user.phone
    form.manifesto.data = current_user.manifesto
    return render_template("user/user_info_modify.html", form=form)


@user_bp.route("/user_password_modify", methods=["GET", "POST"])
@login_required
def user_password_modify():
    form = UserChangePasswordForm()
    if form.is_submitted():
        if form.validate():
            if current_user.check_password(form.old.data):
                current_user.password = form.new.data
                try:
                    db.session.commit()
                    flash("太棒了 ❤ 密码修改成功！请重新登陆！")
                    logout_user()
                    return redirect(url_for("user.login"))
                except Exception:
                    flash("密码修改失败 😱 请联系管理员！")
                    db.session.rollback()
            else:
                flash("旧密码不正确 😱 再想想！")
            return redirect(url_for("user.user_password_modify"))
        else:
            flash("哎呀 😱 请检查输入是否正确！")
    return render_template("user/user_password_modify.html", form=form)


@user_bp.route("/follow", methods=["POST"])
@login_required
def follow():
    json = request.get_json()
    followed_id = json.get("followed_id")
    follow_flag = json.get("follow_flag")
    if followed_id and follow_flag in (0, 1):
        followed = User.query.filter_by(id=followed_id).first()
        if follow_flag == 1:
            if current_user.follow(followed):
                is_followed = current_user.is_followed_by(followed)
                res = {"status": "ok", "msg": "follow", "is_followed": is_followed}
                response_code = 200
            else:
                res = {"status": "error", "msg": "repeat follow"}
                response_code = 400
        elif follow_flag == 0:
            if current_user.unfollow(followed):
                is_followed = current_user.is_followed_by(followed)
                res = {"status": "ok", "msg": "cancel follow", "is_followed": is_followed}
                response_code = 200
            else:
                res = {"status": "error", "msg": "have not followed"}
                response_code = 400
    else:
        res = {"status": "error", "msg": "error argument"}
        response_code = 400
    return jsonify(res), response_code


@user_bp.route("user_follow/<follow_relation>/<int:user_id>/<int:page>")
@login_required
def user_following(follow_relation, user_id, page=1):
    if follow_relation == "following":
        pagination = Follow.query.filter_by(follower_id=user_id).order_by(Follow.timestamp.desc()).paginate(page, 50)
        follow_list = pagination.items
    elif follow_relation == "followers":
        pagination = Follow.query.filter_by(followed_id=user_id).order_by(Follow.timestamp.desc()).paginate(page, 50)
        follow_list = pagination.items
    return render_template("user/user_follow.html", follow_relation=follow_relation,  follow_list=follow_list, pagination=pagination, user_id=user_id)