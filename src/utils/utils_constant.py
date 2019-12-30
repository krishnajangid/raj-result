#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import enum

BASE_URL = 'http://rajresults.nic.in/{url}'


@enum.unique
class RajUrl(enum.Enum):
    SSLC = BASE_URL.format(url='resbserx19.asp')
    ARTS = BASE_URL.format(url='rajartsbser2019.asp')
    COMMERCE = BASE_URL.format(url='commercebser19.asp')
    SCIENCE = BASE_URL.format(url='sciencebser19.asp')


@enum.unique
class ActionTypeEnum(enum.Enum):
    POST = 'POST'
    GET = 'GET'
    DELETE = 'DELETE'
    PUT = 'PUT'


@enum.unique
class StatusTypeEnum(enum.Enum):
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    IN_PROGRESS = 'IN PROGRESS'
