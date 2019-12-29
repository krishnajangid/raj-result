#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import json

import flask_admin as admin
from flask import redirect, url_for, request, abort
from flask_admin import expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import (Security, SQLAlchemyUserDatastore, current_user, login_required,
                            roles_required, roles_accepted)
from models import (User, Role)
from utils_constant import ActionTypeEnum, StatusTypeEnum
from utils_response import RestResponse
from webapp import app, db

user_data_store = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_data_store)


# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        get_url=url_for
    )


class RoleSuperuser(ModelView):
    def is_accessible(self):
        return current_user.is_active and current_user.is_authenticated and current_user.has_role('superuser')


class MyModelView(ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.has_role('superuser') or current_user.has_role('admin')
                )

    @property
    def can_create(self):
        return current_user.has_role('superuser')

    @property
    def can_edit(self):
        return current_user.has_role('superuser')

    @property
    def can_delete(self):
        return current_user.has_role('superuser')

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))


@app.route('/')
def index():
    return redirect("/admin")


class HomeView(AdminIndexView):

    @expose('/')
    @login_required
    def index(self):
        return self.render('admin/index.html')


# ===================== Model Views ===================
class UsersView(ModelView):

    def __init__(self, session, **kwargs):
        super(UsersView, self).__init__(User, session, **kwargs)

    column_list = ('email', 'active', 'confirmed_at', 'roles', '')
    column_searchable_list = ('email',)

    can_view_details = True
    column_display_actions = True
    can_delete = False
    page_size = 15


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The page could not be found.</p>", 404


@app.route("/raj-result/add/", methods=[ActionTypeEnum.POST.value])
def add_data():
    request_data = request.json
    print(request_data.get('Roll Number'))
    return RestResponse.get(StatusTypeEnum.SUCCESS.value)


@app.route("/raj-result/update/", methods=[ActionTypeEnum.POST.value])
def update_data():
    request_data = request.json
    return RestResponse.get(StatusTypeEnum.SUCCESS.value)


@app.route("/raj-result/delete/", methods=[ActionTypeEnum.POST.value])
def delete_data():
    request_data = request.json
    return RestResponse.get(StatusTypeEnum.SUCCESS.value)


@app.route("/raj-result/get-one/", methods=[ActionTypeEnum.POST.value])
def get_one():
    return RestResponse.get(StatusTypeEnum.SUCCESS.value)


@app.route("/raj-result/get-all/", methods=[ActionTypeEnum.POST.value])
def get_all():
    return RestResponse.get(StatusTypeEnum.SUCCESS.value)


# Create admin
admin = admin.Admin(
    app,
    name='Raj Result',
    template_mode='bootstrap3',
    index_view=HomeView()
)

admin.add_view(UsersView(db.session))
