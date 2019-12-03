#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging

from flask import Flask
from flask import jsonify

flask_app = Flask(__name__)

logger = logging.getLogger(__name__)


class RestResponse(object):

    @classmethod
    def get(cls, status, result=None, status_code=200, message='', _type='', **kwargs):
        """
        Create final request object
        """
        data = {'type': _type, 'status': status, 'message': message}
        if kwargs:
            data['additional_data'] = kwargs
        if result is not None:
            data['data'] = result
        content = jsonify(data)
        return flask_app.make_response((content, status_code))
