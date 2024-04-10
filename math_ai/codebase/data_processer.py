# -*- coding: utf-8 -*-
# Date       : 2023/4/3
# Author     : @ Xin Cheng
# email      :
# Description: 将原始的PDF题目处理成为dataset的格式 JSON 文件
from typing import List, Dict

import json
# TODO 这个地方Load JSON，然后每次给一个字典，给到下一阶段，完成之后重复给字典的过程。

class DataProcesser:
    def __init__(self):
        pass

    def run(self) -> List[Dict]:
        """
        {
            "desc":"<QUESTION DESC>",
            "type":"<select from human design>",
        }
        """
        return {"<example>"}
    

    def load_data(self):
        """
        Load JSON 文件
        """
        pass

if __name__ == "__main__":
    d = DataProcesser()
    data = d.load_data()
    