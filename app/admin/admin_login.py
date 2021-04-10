from flask_admin.contrib import sqla
import flask_login as login
import flask_admin as admin
from flask_admin import helpers, expose
from flask import redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app.form.admin import AdminUserLoginForm
from flask import request


# Create customized model view class
class AdminModelView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated and login.current_user.is_admin


# Create customized index view class that handles login & registration
class AdminIndexView(admin.AdminIndexView):

    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(AdminIndexView, self).index()

    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = AdminUserLoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

            if login.current_user.is_authenticated:
                return redirect(url_for('.index'))
            else:
                flash("您不是管理员.")
        self._template_args['form'] = form
        return super(AdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))
