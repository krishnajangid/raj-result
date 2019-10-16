#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import enum


@enum.unique
class UserEnum(enum.Enum):
    UserList = ["Roll Number", "Candidate Name", "Father's Name", "Mother's Name", "School/Center's Name"]
