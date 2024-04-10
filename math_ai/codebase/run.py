# -*- coding: utf-8 -*-
# Date       : 2023/4/3
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: run math ai

from math_ai.codebase.gate_controller import GateController
from math_ai.codebase.math_resovler import MathResolver
from math_ai.codebase.data_processer import DataProcesser
from math_ai.codebase.solution_refiner import SolutionRefiner
from metagpt.roles.di.data_interpreter import DataInterpreter

def solution(question_path:str):
    pass

# 1. 将RUN函数串起来
# 2. 为Resolver 构建不同的Phase函数
# 3. 思考Refiner，是如何根据思考过程与题干给出合适答案的
# 4. 
