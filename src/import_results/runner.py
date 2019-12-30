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

    def __init__(self, base_url):
        self.__raj_bord_obj = RajResult(base_url)
        self.__request = MakeRequest('http://localhost:9898/raj-result/add/', is_josn=True)

    def process(self, reg_no, branch):
        self.__raj_bord_obj.process(reg_no)
        result_dict = self.__raj_bord_obj.result_dict
        result_dict['branch'] = branch
        result_dict['year'] = 2019
        self.save_result(result_dict)
        print(json.dumps(result_dict, indent=4))

    def save_result(self, result_dict):
        self.__request.post_data = result_dict
        self.__request.post()


extractor_base = ProcessResult(base_url=RajUrl.SSLC.value)
for reg_no in [1429382]:
    extractor_base.process(reg_no, RajUrl.SSLC.name)


extractor_base = ProcessResult(base_url=RajUrl.COMMERCE.value)
for reg_no in [2800001]:
    extractor_base.process(reg_no, RajUrl.COMMERCE.name)

extractor_base = ProcessResult(base_url=RajUrl.SCIENCE.value)
for reg_no in [2528939]:
    extractor_base.process(reg_no, RajUrl.SCIENCE.name)
