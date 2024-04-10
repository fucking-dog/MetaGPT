# -*- coding: utf-8 -*-
# Date       : 2023/4/3
# Author     : @Jiayi Zhang @ Fengwei Teng @ Yi Huang
# email      :
# Description: The Math Resolver is a core component of Math AI. Here, the Math Resolver will develop a plan based on the problem description and the strategy of the Gate Controller, selecting or recreating phase from the existing phase library, and invoking the LLM for solution finding.


from typing import Dict
from metagpt.roles.di.data_interpreter import DataInterpreter
from math_ai.codebase.engine.llm import OpenAILLM
from math_ai.codebase.prompt import resolver_planner

# TODO add different phase in codebase.phase

async def main(requirement: str = ""):
    di = DataInterpreter()
    await di.run(requirement)

class MathResolver:
    def __init__(self):
        self.llm = OpenAILLM()
        self.role = "You're the most powerful math Olympiad in the world."
        self.llm.set_role(self.role)

    def run(self, problem: Dict, types: Dict) -> Dict:
        """
        Math Resolver resolve the problem based on the strategy from Gate Controller.
        First, math resolver need to develop a plan which contains basic phase (di for compute; logic validate for judge solution) to solve the problem.
        Then, math resolver need to ? <It's Complex Stage>
        Finally, math resolver need to return the solution without refine.
        """
        strategy = types["strategy"]
        problem_multiple = types["multiple"]
        # 1. 直接要求他解决数学问题，思考这个过程。 zero shot 让他先去对这个题目给出一个计划。
        # 2. 得到这个过程之后，让他结合我们的strategy 跟 Prompt，重新构建phase
        # 3. 每一个Phase的Prompt如何去写 
        plan = self.llm.llm_response(prompt=resolver_planner.format(problem_desc=problem["desc"], strategy=strategy), json_mode=True)
        # 解决方法 —— Prompt对每一个Phase都限制输出格式
        for phase in plan:
            if phase["phase"] == "di":
                phase["solution"] = self.di_run(problem)
            elif phase["phase"] == "logic_validate":
                phase["solution"] = self.logic_validate(problem)
            elif phase["phase"] == "merge":
                phase["solution"] = self.merge()
            elif phase["phase"] == "finish":
                phase["solution"] = self.finish()

        return {"solution": "<content>"}
    
    def di_run(self, problem):
        
        return "Hello world"
    