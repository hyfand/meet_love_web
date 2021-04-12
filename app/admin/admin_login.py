from flask_login import current_user, login_user, logout_user
import flask_admin as admin
from flask_admin.contrib import sqla
from flask_admin import helpers, expose
from flask_admin.form import SecureForm
from flask import redirect, url_for, flash
from app.form.admin import AdminUserLoginForm
from flask import request


# Create customized model view class
class AdminModelView(sqla.ModelView):

    form_base_class = SecureForm

    can_view_details = True
    create_modal = True
    edit_modal = True

    column_exclude_list = ["to_share", "share"]

    column_searchable_list = ["content"]
    # column_filters = ['content']

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('admin.login_view', next=request.url))

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
