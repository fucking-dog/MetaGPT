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

import json
from ..data_processer import DataProcesser
from ..gate_controller import GateController
from ..math_resovler import MathResolver

def solution(question_path:str):
    solutions = dict()
    dp = DataProcesser()
    gc = GateController()
    mr = MathResolver()
    sr = SolutionRefiner()

    problem_dict_list = dp.run() # List[Dict]
    for problem_dict in problem_dict_list:
        strategy_dict = gc.run(problem_dict)
        solution = mr.run(problem_dict, strategy_dict)
        final_solution = sr.run(problem_dict, strategy_dict, solution)


