# -*- coding: utf-8 -*-
# Date       : 2023/4/3
# Author     : @ Xin Cheng
# email      :
# Description: 将原始的PDF题目处理成为dataset的格式 JSON 文件
from typing import List, Dict

# TODO 这个地方不提交，最后手动就 OK

class DataProcesser:
    def __init__(self):
        pass

    def run(self) -> List[Dict]:
        """
        {
            "desc":"<QUESTION DESC>",
            "type":"<select from human design>",
            "image":{
                "exist": "<bool>",
                "base64": "<base64 encode>"
            }
        }
        """
        return [{},{}]