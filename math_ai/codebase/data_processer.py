# -*- coding: utf-8 -*-
# Date       : 2023/4/3
# Author     : @ Xin Cheng
# email      :
# Description: 将原始的PDF题目处理成为dataset的格式 JSON 文件
from typing import List, Dict

import json
import copy
# TODO 这个地方Load JSON，然后每次给一个字典，给到下一阶段，完成之后重复给字典的过程。

class DataProcesser:
    def __init__(self):
        pass

    def run(self, question_path) -> List[Dict]:
        """
        {
            "desc":"<QUESTION DESC>",
            "type":"<select from human design>",
        }
        """

        # 从JSON文件中读取数据并转换为字典
        with open(question_path, 'r') as f:
            problem_dict = json.load(f)

        problem_dict_list = []
        for value in problem_dict.values():
            value['desc'] = copy.deepcopy(value['description'])
            problem_dict_list.append(value)

        return problem_dict_list
    



if __name__ == "__main__":
    d = DataProcesser()


