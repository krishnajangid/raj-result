#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import json
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

        student_info_dict = self.__get_student_info(soup_data)
        student_result_dict = self.__get_student_marks(soup_data)
        student_data = {
            'student_info': student_info_dict,
            'result': student_result_dict
        }
        print(json.dumps(student_data, indent=4))

    @staticmethod
    def __get_student_info(soup_data):
        info_table = soup_data.find('table', {'style': 'border-collapse: collapse'}).text.strip().split('\n')
        student_info_list = []
        for student_data in info_table:
            data = student_data.strip()
            if data and (data not in UserEnum.UserList.value):
                student_info_list.append(data)

        student_info_dict = {
            'reg_num': student_info_list[0],
            'name': student_info_list[1],
            'father_name': student_info_list[2],
            'mother_name': student_info_list[3],
            'school': student_info_list[4],
        }
        return student_info_dict

    @staticmethod
    def __get_student_marks(soup_data):
        result_dict_list = []
        info_table = soup_data.find_all('table', {'style': 'border-collapse: collapse'})[1]
        for tr_info in info_table.find_all('tr')[1:7]:
            result_list = []
            for td_info in tr_info.find_all('td'):
                result_list.append(td_info.text.strip())
            result_dict = {
                'sub_name': result_list[0],
                'theory': result_list[1],
                'sessional': result_list[3],
                'th_ss': result_list[4],
                'practical': result_list[5],
            }
            result_dict_list.append(result_dict)
        return result_dict_list


extractor_base = ExtractorBase()
for reg_no in [1429382, 1429381, 1429383, 1429385]:
    extractor_base.process(reg_no)
    print("===="*20)
