from flask import Blueprint, render_template, flash, redirect, url_for
from app.form.user import UserRegisterForm, UserLoginForm, UserChangeInfoForm, UserChangePasswordForm, UserPortraitForm
from app.models.user import *
from app.extensions import db
from flask_login import login_user, logout_user, current_user, login_required
from app.utils import redirect_back, random_filename
from app.uploads_set import potrait


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
                real_name=form.real_name.data,
                id_number=form.id_number.data,
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


@user_bp.route("/user_protrait_modify", methods=["GET", "POST"])
@login_required
def user_protrait_modify():
    form = UserPortraitForm()
    if form.validate_on_submit():
        name = random_filename(form.potrait.data.filename)
        potrait_name = potrait.save(form.potrait.data, name=name)
        current_user.potrait = potrait_name
        db.session.commit()
        return redirect_back()
    return render_template("user/user_potrait_modify.html", form=form)


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