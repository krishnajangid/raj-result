#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import logging

from bs4 import BeautifulSoup

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

        info_table = soup_data.find('table', {'style': 'border-collapse: collapse'}).text
        user_data = info_table.strip().split('\n')

        print(info_table.strip().split('\n'))
        print(" ".join(info_table.split()))
        print(type(info_table))




x = ExtractorBase()
print(x.process())


'''


r = requests.get('http://rajresults.nic.in/resbserx19.asp', data={'roll_no': 1429382, 'B1': 'Submit'}, headers={'Referer':'http://rajresults.nic.in/resbserx19.htm'})
# print(r.text)
data = BeautifulSoup(r.text, features="html5lib")
table_list = data.find_all('table')
print(table_list)

'''
