# -*- coding: utf-8 -*-
# Date       : 2023/4/3
# Author     : @Jiayi Zhang @ Fengwei Teng @ Yi Huang
# email      :
# Description: The Math Resolver is a core component of Math AI. Here, the Math Resolver will develop a plan based on the problem description and the strategy of the Gate Controller, selecting or recreating phase from the existing phase library, and invoking the LLM for solution finding.


from typing import Dict
from metagpt.roles.di.data_interpreter import DataInterpreter
# TODO add different phase in codebase.phase
from math_ai.codebase.engine.llm import OpenAILLM


class MathResolver:
    def __init__(self):
        self.llm = OpenAILLM()
        self.role = "<TODO Here is Math Resolver's system prompt>"
        self.llm.set_role(self.role)

    def run(self, problem: Dict, strategy: Dict) -> Dict:
        """
        Math Resolver resolve the problem based on the strategy from Gate Controller.
        First, math resolver need to develop a plan which contains basic phase (di for compute; logic validate for judge solution) to solve the problem.
        Then, math resolver need to ? <It's Complex Stage>
        Finally, math resolver need to return the solution without refine.
        """
        return {"solution": "<content>"}