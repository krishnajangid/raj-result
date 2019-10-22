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
    def get(cls, status: str, result: (dict, None) = None, status_code: int = 200, message: str = '', _type: str = '',
            **kwargs) -> Flask.make_response:
        """
        Create final request object
        """
        data = {'type': _type, 'status': status, 'message': message}
        if kwargs:
            data['additional_data'] = kwargs
        if result is not None:
            data['data'] = result
        logger.debug(json.dumps(data, indent=4))
        content = jsonify(data)
        return flask_app.make_response((content, status_code))
