#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import logging

from utils_extractor_base import ExtractorBase

logger = logging.getLogger(__name__)


class RajResult(object):

    def __init__(self, base_url):
        self.__extractor_base_obj = ExtractorBase(base_url)
        self.__result_dict = None

    @property
    def result_dict(self):
        return self.__result_dict

    @result_dict.setter
    def result_dict(self, result_dict):
        self.__result_dict = result_dict

    def process(self, roll_no):
        soup_data = self.__extractor_base_obj.process(roll_no)
        if soup_data:
            self.result_dict = self.__get_student_result(soup_data)

    @staticmethod
    def __get_student_result(soup_data):
        student_info_dict = {}
        center_data = soup_data.find('center')
        for table_data in center_data.find_all('table'):
            student_dict = {'marks': []}
            for table_tr_data in table_data.find_all('tr'):
                table_td_data_list = table_tr_data.find_all('td')
                if len(table_td_data_list) == 6:
                    result_list = [table_td_data.text.strip() for table_td_data in table_td_data_list]
                    try:
                        _ = int(result_list[1])
                    except ValueError:
                        continue
                    result_dict = {
                        'sub_name': result_list[0],
                        'theory': result_list[1],
                        'sessional': result_list[3],
                        'th_ss': result_list[4],
                        'practical': result_list[5],
                        'total': result_list[5],
                    }
                    student_dict['marks'].append(result_dict)
                elif len(table_td_data_list) == 2:
                    student_dict[table_td_data_list[0].text.strip()] = table_td_data_list[1].text.strip()
            student_info_dict.update(student_dict)

        return student_info_dict
