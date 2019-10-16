#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import json
import logging
from typing import Dict

import requests
from requests.adapters import HTTPAdapter

from utils_exception import (BaseUrlNotFound, ResponseCodeException, JsonDecodeError, ConnectionTimeOut)
from urllib3 import Retry

logger = logging.getLogger(__name__)


class MakeRequest(object):
    def __init__(self, base_url=None):
        self.__user_agent = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        self.__time_out = 20
        self.__retry = True
        self.__retry_count = 3
        self.__retry_delay = 0.3  # 0.3 sec
        self.__status_forcelist = [500, 502, 504]
        self.__base_url = base_url

        self.__header_dict = dict()
        self.__session = None

    @property
    def session(self):
        if self.__session is None:
            self.__session = requests.Session()
            logger.debug("Setting request session.")
            retry = Retry(
                total=self.__retry_count,
                read=self.__retry_count,
                connect=self.__retry_count,
                backoff_factor=self.__retry_delay,
                status_forcelist=self.__status_forcelist)

            adapter = HTTPAdapter(max_retries=retry)
            user_agent = self.__user_agent
            logger.debug(f"Setting default user agent as {user_agent}")
            self.__session.headers.update({
                'User-Agent': user_agent
            })
            if self.header_dict:
                self.__session.headers.update(self.header_dict)
            self.__session.mount('http://', adapter)
            self.__session.mount('https://', adapter)
        else:
            logger.debug("Using old session for request.")
        return self.__session

    @property
    def request_timeout(self):
        return self.__time_out

    @property
    def base_url(self):
        return self.__base_url

    @base_url.setter
    def base_url(self, url: str):
        self.__base_url = url

    @property
    def header_dict(self) -> Dict:
        return self.__header_dict

    @header_dict.setter
    def header_dict(self, header_dict: Dict):
        if self.__session:
            self.__session.headers.update(header_dict)
        else:
            self.__session = self.session
            self.__session.headers.update(header_dict)
        self.__header_dict.update(header_dict)

    def add_header(self, key, value):
        self.__header_dict[key] = value

    @property
    def post_data(self):
        return self.__post_data

    @post_data.setter
    def post_data(self, payload):
        self.__post_data = payload

    def post(self):
        try:
            response = self.session.post(url=self.base_url, data=self.post_data, timeout=self.__time_out)
            if response.status_code != 200:
                msg = f"Failure response status code {response.status_code}"
                raise ResponseCodeException(msg)

            return response.text
        except(requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.Timeout) as e:
            err_msg = f"Error: {str(e)}"
            raise ConnectionTimeOut(err_msg)

    def get(self):
        response = self.session.get(self.base_url)
        return response

