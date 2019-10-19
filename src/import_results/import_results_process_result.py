#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import json

from import_results.import_engine_raj_board import RajResult
from utils_constant import RajUrl


class ProcessResult(object):

    def __init__(self, base_url):
        self.__raj_bord_obj = RajResult(base_url)

    def process(self, reg_no):
        self.__raj_bord_obj.process(reg_no)
        result_dict = self.__raj_bord_obj.result_dict
        print(json.dumps(result_dict, indent=4))

    def save_result(self):
        ...


extractor_base = ProcessResult(base_url=RajUrl.RAJ_BOARD.value)
for reg_no in [1429382]:
    extractor_base.process(reg_no)

extractor_base = ProcessResult(base_url=RajUrl.COM_BOARD.value)
for reg_no in [2800001]:
    extractor_base.process(reg_no)

extractor_base = ProcessResult(base_url=RajUrl.SCI_BOARD.value)
for reg_no in [2528939]:
    extractor_base.process(reg_no)
