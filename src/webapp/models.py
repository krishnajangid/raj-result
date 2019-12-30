#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

from flask_security import UserMixin, RoleMixin
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, Boolean)
from sqlalchemy.orm import relationship

from webapp import db


# Define models
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = Column(Integer(), primary_key=True)
    name = Column(String(50), unique=True)

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    roles_users = db.Table(
        'roles_users',
        Column('user_id', Integer(), ForeignKey(f'{__tablename__}.id')),
        Column('role_id', Integer(), ForeignKey('role.id'))
    )
    id = Column(Integer, primary_key=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    active = Column(Boolean())
    confirmed_at = Column(DateTime())

    roles = relationship(Role, secondary=roles_users, backref=db.backref(__tablename__, lazy='dynamic'))

    def __str__(self):
        return self.email


class Branch(db.Model):
    __tablename__ = 'branch'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    cls = Column(String(20), nullable=False)
    created = Column(DateTime, nullable=True)

    def __str__(self):
        return self.name


class School(db.Model):
    __tablename__ = 'school'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    code = Column(String(4), nullable=False)
    created = Column(DateTime, nullable=True)

    def __str__(self):
        return self.name


class Student(db.Model):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True)
    school_id = Column(Integer, ForeignKey(f'school.id'), nullable=False)
    branch_id = Column(Integer, ForeignKey(f'branch.id'), nullable=False)
    reg_num = Column(Integer, nullable=False)
    name = Column(String(50), nullable=False)
    father_name = Column(String(50), nullable=False)
    mother_name = Column(String(50), nullable=False)
    views = Column(Integer, default=0)
    last_views = Column(DateTime)
    year = Column(String(5))
    created = Column(DateTime)
    updated = Column(DateTime)

    school_obj = relationship(School, backref='school')
    branch_obj = relationship(Branch, backref='branch')

    def __str__(self):
        return self.name


class Subject(db.Model):
    __tablename__ = 'subject'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class Marks(db.Model):
    __tablename__ = 'marks'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey(f'student.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey(f'subject.id'), nullable=False)
    theory = Column(Integer, nullable=True)
    sessional = Column(Integer, nullable=True)
    th_ss = Column(Integer, nullable=True)
    practical = Column(Integer, nullable=True)
    total = Column(String, nullable=False)
    subject_obj = relationship(Subject, backref='subject')


    def __str__(self):
        return self.name
