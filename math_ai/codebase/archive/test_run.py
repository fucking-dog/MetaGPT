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


def solution(question_path:str):
    dp = DataProcesser()
    dp.load_data()
    question_json = dp.run()

    gc = GateController()
    strategy_dict = gc.run(question_json)


    pass


if __name__ == "__main__":
    solution("")