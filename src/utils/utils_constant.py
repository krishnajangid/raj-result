#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import enum

BASE_URL = 'http://rajresults.nic.in/{url}'


@enum.unique
class RajUrl(enum.Enum):
    RAJ_BOARD = BASE_URL.format(url='resbserx19.asp')
    ARTS_BOARD = BASE_URL.format(url='rajartsbser2019.asp')
    COM_BOARD = BASE_URL.format(url='commercebser19.asp')
    SCI_BOARD = BASE_URL.format(url='sciencebser19.asp')
