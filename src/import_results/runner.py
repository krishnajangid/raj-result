#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import json
import logging
import sys
from inspect import getframeinfo, currentframe
from pathlib import Path


filename = getframeinfo(currentframe()).filename
current_module_path = Path(filename).resolve().parent

ROOT_PATH = Path(current_module_path).parents[0].as_posix()

module_path_list = [
    f"{ROOT_PATH}/utils",
    f"{ROOT_PATH}/import_results",
    f"{ROOT_PATH}/webapp",
]

for index, path in enumerate(module_path_list):
    sys.path.insert(index, path)


from import_engine_raj_board import RajResult
from utils_constant import RajUrl
from utils_request import MakeRequest


class ProcessResult(object):

    def __init__(self):
        self.__request = MakeRequest('http://localhost:9898/raj-result/add/', is_josn=True)

    def process(self, reg_no):
        base_url = None
        branch = None
        if 2500001 <= reg_no <= 2760618:
            base_url = RajUrl.SCIENCE.value
            branch = RajUrl.SCIENCE.name
        elif 2800001 <= reg_no <= 2842146:
            base_url = RajUrl.COMMERCE.value
            branch = RajUrl.COMMERCE.name
        elif 2900001 <= reg_no <= 3476838:
            base_url = RajUrl.ARTS.value
            branch = RajUrl.ARTS.name
        elif 1300001 <= reg_no <= 2434470:
            base_url = RajUrl.SSLC.value
            branch = RajUrl.SSLC.name

        if base_url:
            raj_bord_obj = RajResult(base_url)
            raj_bord_obj.process(reg_no)
            result_dict = raj_bord_obj.result_dict

            result_dict['branch'] = branch
            result_dict['year'] = 2019
            self.save_result(result_dict)

            print(json.dumps(result_dict, indent=4))

    def save_result(self, result_dict):
        self.__request.post_data = result_dict
        self.__request.post()


extractor_base = ProcessResult()
for reg_no in range(1300001, 1400001, 10):
    if reg_no == 1500001:
        break
    extractor_base.process(reg_no)
