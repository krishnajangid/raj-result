#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import logging

from bs4 import BeautifulSoup

from utils_constant import UserEnum
from utils_exception import JsonDecodeError, ResponseCodeException, ConnectionTimeOut
from utils_request import MakeRequest

logger = logging.getLogger(__name__)


class ExtractorBase(object):

    def __init__(self):
        self.__request = MakeRequest(base_url='http://rajresults.nic.in/resbserx19.asp')

    def process(self, roll_no=1429382):
        self.__request.post_data = {'roll_no': roll_no, 'B1': 'Submit'}
        self.__request.add_header('Referer', 'http://rajresults.nic.in/resbserx19.htm')

        response_data = None

        try:
            response_data = self.__request.post()
        except (JsonDecodeError, ResponseCodeException, ConnectionTimeOut) as e:
            print(e)
            logger.error(f"Error while getting data. {e}")
        try:
            soup_data = BeautifulSoup(response_data, features="html5lib")
        except TypeError:
            logger.error(f"Error while Soup data {response_data}")
            return None

        info_table = soup_data.find('table', {'style': 'border-collapse: collapse'}).text.strip().split('\n')

        user_info = []
        for user_data in info_table:
            data = user_data.strip()
            if data and (data not in UserEnum.UserList.value):
                user_info.append(data)

        user_dict = {
            'reg_num': user_info[0],
            'name': user_info[1],
            'father_name': user_info[2],
            'mother_name': user_info[3],
            'school': user_info[4],
        }
        print(user_dict)


x = ExtractorBase()
print(x.process())

