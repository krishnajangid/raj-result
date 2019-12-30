#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import json
import re
from datetime import datetime

import flask_admin as admin
from flask import Markup, redirect, url_for, request, abort
from flask_admin import expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import (Security, SQLAlchemyUserDatastore, current_user, login_required,
                            roles_required, roles_accepted)
from models import (User, Role, Subject, School, Branch, Student, Marks)
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

    @expose('/student-info/<int:student_id>')
    @roles_accepted('superuser', 'admin')
    def student_info(self, student_id):
        student_result_dict = Student.query.add_columns(
            Student.name, Student.mother_name, Student.reg_num, Student.father_name, Student.views,
            Student.created, Student.last_views, Student.year, Student.updated, School.name.label('school_name'),
            School.code, Branch.name.label('branch_name'),
        ).filter(
            Student.school_id == School.id,
            Student.branch_id == Branch.id,
            Student.id == student_id
        ).one()

        marks_result_dict_list = Marks.query.add_columns(
            Marks.total, Marks.theory, Marks.sessional, Marks.th_ss, Marks.practical, Subject.name
        ).filter(
            Subject.id == Marks.subject_id,
            Marks.student_id == student_id
        ).all()

        print(student_result_dict)
        print("==-"*30)
        score = [int(re.search(r'\d+', marks_dict.total).group()) for marks_dict in marks_result_dict_list]

        return self.render('admin/student_info.html', marks_result_dict_list=marks_result_dict_list,
                           student_result_dict=student_result_dict, score=score)


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


class StudentView(ModelView):

    def __init__(self, session, **kwargs):
        super(StudentView, self).__init__(Student, session, **kwargs)

    column_list = ['reg_num', 'name', 'father_name', 'mother_name', 'views', 'last_views', 'year', 'branch_obj.name',
                   'Action']
    column_searchable_list = ('reg_num', 'name')
    column_sortable_list = column_filters = column_list[0:-1]

    def _link_formatter(view, context, model, name):
        link = f"""<a href='/admin/student-info/{str(model.id)}' class='btn btn-sm btn-success ml-1'>
                <i class='fa fa-eye'></i></a>"""

        return Markup(link)

    column_formatters = {
        'Action': _link_formatter
    }
    column_labels = {
        'branch_obj.name': 'Branch',
    }

    can_view_details = True
    column_display_actions = False
    can_delete = False
    can_create = False
    can_edit = False
    page_size = 15


class MarksView(ModelView):

    def __init__(self, session, **kwargs):
        super(MarksView, self).__init__(Marks, session, **kwargs)

    column_list = ('subject_obj.name', 'theory', 'sessional', 'th_ss', 'practical', 'total')
    column_sortable_list = column_filters = column_list
    column_labels = {
        'subject_obj.name': 'Subject Name',
    }

    column_display_actions = False
    can_delete = False
    can_create = False
    can_edit = False
    page_size = 13


class SubjectView(ModelView):

    def __init__(self, session, **kwargs):
        super(SubjectView, self).__init__(Subject, session, **kwargs)

    column_list = ('name',)
    column_sortable_list = column_filters = column_list

    column_display_actions = False
    can_delete = False
    can_create = False
    can_edit = False
    page_size = 13


class SchoolView(ModelView):

    def __init__(self, session, **kwargs):
        super(SchoolView, self).__init__(School, session, **kwargs)

    column_list = ('code', 'name')
    column_searchable_list = column_list
    column_sortable_list = column_filters = column_list

    column_display_actions = False
    can_delete = False
    can_create = False
    can_edit = False
    page_size = 13


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The page could not be found.</p>", 404


@app.route("/raj-result/add/", methods=[ActionTypeEnum.POST.value])
def add_data():
    request_data_dict = request.json
    school_id = get_create_school(request_data_dict.get("School/Center's Name"))
    branch_id = db.session.query(Branch).filter(Branch.name == request_data_dict["branch"]).first().id

    name = request_data_dict.get("Candidate Name")
    reg_num = request_data_dict.get("Roll Number")
    father_name = request_data_dict.get("Father's Name")
    mother_name = request_data_dict.get("Mother's Name")
    year = request_data_dict.get("year")

    student_id = get_create_student(name, reg_num, father_name, mother_name, school_id, branch_id, year)

    for data_dict in request_data_dict['marks']:
        subject_id = get_create_subject(data_dict['sub_name'])
        theory = data_dict.get('theory')
        sessional = data_dict.get('sessional')
        th_ss = data_dict.get('th_ss')
        practical = data_dict.get('practical') or None
        total = data_dict.get('total')

        create_marks(student_id, subject_id, theory, sessional, th_ss, practical, total)

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


def get_create_student(name, reg_num, father_name, mother_name, school_id, branch_id, year):
    student_obj = db.session.query(Student).filter(Student.reg_num == reg_num, Student.school_id == school_id).first()
    if not student_obj:
        student_obj = Student(name=name, reg_num=reg_num, father_name=father_name, mother_name=mother_name,
                              school_id=school_id, branch_id=branch_id, year=year,
                              created=datetime.now(), updated=datetime.now())
        db.session.add(student_obj)
        db.session.commit()

    return student_obj.id


def get_create_school(school_name):
    school_code, name = school_name.split(') ')[0].strip('('), school_name.split(') ')[1].strip()
    school_obj = db.session.query(School).filter(School.code == school_code, School.name == name).first()
    if not school_obj:
        school_obj = School(code=school_code, name=name, created=datetime.now())
        db.session.add(school_obj)
        db.session.commit()

    return school_obj.id


def get_create_subject(subject_name):
    subject_obj = db.session.query(Subject).filter(Subject.name == subject_name).first()
    if not subject_obj:
        subject_obj = Subject(name=subject_name)
        db.session.add(subject_obj)
        db.session.commit()

    return subject_obj.id


def create_marks(student_id, subject_id, theory, sessional, th_ss, practical, total):
    marks_obj = Marks(student_id=student_id, subject_id=subject_id,
                      practical=practical, th_ss=th_ss,
                      sessional=sessional, theory=theory,
                      total=total)
    db.session.add(marks_obj)
    db.session.commit()


# Create admin
admin = admin.Admin(
    app,
    name='Raj Result',
    template_mode='bootstrap3',
    index_view=HomeView()
)

admin.add_view(UsersView(db.session))
admin.add_view(StudentView(db.session))
admin.add_view(MarksView(db.session))
admin.add_view(SubjectView(db.session))
admin.add_view(SchoolView(db.session))
