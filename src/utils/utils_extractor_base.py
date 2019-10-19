#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import logging

from bs4 import BeautifulSoup

from utils_exception import JsonDecodeError, ResponseCodeException, ConnectionTimeOut
from utils_request import MakeRequest

logger = logging.getLogger(__name__)


class ExtractorBase(object):

    def __init__(self, base_url):
        self.__request = MakeRequest(base_url)
        self.__referer = base_url

    def process(self, roll_no):
        self.__request.post_data = {'roll_no': roll_no, 'B1': 'Submit'}
        self.__request.add_header('Referer', self.__referer)

        try:
            response_data = self.__request.post()
        except (JsonDecodeError, ResponseCodeException, ConnectionTimeOut) as e:
            logger.error(f"Error while getting data. {e}")
            return None
        try:
            return BeautifulSoup(response_data, features="html5lib")
        except TypeError:
            logger.error(f"Error while Soup data {response_data}")
            return None
