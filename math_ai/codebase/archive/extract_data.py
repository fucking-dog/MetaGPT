# -*- coding: utf-8 -*-
# Date       : 2023/3/29
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: Extract Level 5 question from math dataset

import os
import json
DATA_SET_PATH = "/math_ai/dataset/math/test.json"
LEVEL_5_PATH = "/math_ai/dataset/math/level_5.jsonl"
problems = []
with open(DATA_SET_PATH,"r") as d:
    for line in d:
        problems.append(json.loads(line))

level_5_problems = []
for problem in problems:
    if problem["level"] == "Level 5":
        level_5_problems.append(problem)

import json

level_5_problems = []
level_5_type = []
for problem in problems:
    if problem["level"] == "Level 5":
        level_5_problems.append(problem)
    if problem["type"] not in level_5_type:
        level_5_type.append(problem["type"])      
print(level_5_type)

for k,v in level_5_problems[0].items():
    print(level_5_problems[0])
    print(k)


# 将级别为5的问题存储为jsonl文件
# with open(LEVEL_5_PATH, 'w', encoding='utf-8') as file:
#     for problem in level_5_problems:
#         json.dump(problem, file, ensure_ascii=False)
#         file.write('\n')
