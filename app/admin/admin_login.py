from flask_login import current_user, login_user, logout_user
import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin import helpers, expose
from flask import redirect, url_for, flash
from app.form.admin import AdminUserLoginForm
from flask import request


# Create customized model view class
class AdminBaseModelView(sqla.ModelView):

    # can_view_details = True
    create_modal = True
    edit_modal = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('admin.login_view', next=request.url))


class AdminShareModelView(AdminBaseModelView):
    column_exclude_list = ["to_share", "share", "img"]
    column_searchable_list = ["content", "author.nick_name"]
    column_filters = ["id", "content", "author_id", "author.nick_name"]
    column_display_pk = True

class AdminCommentModelView(AdminBaseModelView):
    column_exclude_list = []
    column_searchable_list = ["content"]
    column_filters = ["content"]

class AdminUserModelView(AdminBaseModelView):
    column_exclude_list = ["avatar_s", "avatar_m", "avatar_l", "avatar_row", "password_hash"]
    column_searchable_list = ["user_name"]
    column_filters = ["id", "user_name", "nick_name"]
    column_display_pk = True

# Create customized index view class that handles login & registration
class AdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for(".login_view"))
        return super(AdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = AdminUserLoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login_user(user)

            if current_user.is_authenticated and current_user.is_admin:
                flash("登录成功.")
                return redirect(url_for('.index'))

        self._template_args['form'] = form
        return super(AdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))
