# -*- coding: utf-8 -*-
# Date       : 2023/4/3
# Author     : @Jiayi Zhang @ Fengwei Teng @ Yi Huang
# email      :
# Description: The Math Resolver is a core component of Math AI. Here, the Math Resolver will develop a plan based on the problem description and the strategy of the Gate Controller, selecting or recreating phase from the existing phase library, and invoking the LLM for solution finding.


from typing import Dict
from metagpt.roles.di.data_interpreter import DataInterpreter
from math_ai.codebase.engine.llm import OpenAILLM
from math_ai.codebase.prompt import zero_shot_planner, resolver_planner, inference_prompt, di_prompt, result_validate_prompt, inference_final_prompt, logic_validate_prompt
from math_ai.codebase.strategies import get_strategy_desc


class MathResolver:
    def __init__(self):
        self.llm = OpenAILLM()
        self.role = "You're the most powerful math Olympiad in the world."
        self.llm.set_role(self.role)

    def run(problem:Dict, types:Dict):
        """
        problem: Dict
        types: {"strategy":"", "decompose":""} 
        """
        return {"current_trajectory": "current_trajectory"}

    async def single_run(self, problem: Dict, types: Dict) -> Dict:
        """
        Math Resolver resolve the problem based on the strategy from Gate Controller.
        First, math resolver need to develop a plan which contains basic phase (di for compute; logic validate for judge solution) to solve the problem.
        Then, math resolver need to ? <It's Complex Stage>
        Finally, math resolver need to return the solution without refine.
        """
        strategy_name = types["strategy"]
        type_decompose = "多个问题" if types["if_muti"] == "muti" else "simple"
        strategy = get_strategy_desc(strategy_name)

        origin_plan = self.llm.llm_response(prompt=zero_shot_planner.format(problem_desc=problem["description"]))
        resolver_plan = self.llm.llm_response(prompt=resolver_planner.format(problem_desc=problem["description"], strategy=strategy, origin_plan=origin_plan, type_decompose=type_decompose, type_problem=problem["type"]), json_mode=True)
        print(resolver_plan)
        current_trajectory = []
        for index, phase in enumerate(resolver_plan["plan"]):
            if phase["phase"] == "inference":
                answer = self.inference(problem, current_trajectory, subgoal=phase["desc"])
                current_trajectory.append({"plan":phase["desc"],"reason":phase["reason"],"answer":answer})
            elif phase["phase"] == "di":
                answer = await self.di_run(problem, current_trajectory, subgoal=phase["desc"])
                current_trajectory.append({"plan":phase["desc"],"reason":phase["reason"],"answer":answer})
            elif phase["phase"] == "logic_validate":
                result = self.logic_validate(problem, current_trajectory, subgoal=phase["desc"])
                if result["judge"]:
                    current_trajectory.append({"plan":phase["desc"],"reason":phase["reason"],"answer":"逻辑正确"})
                else:
                    current_trajectory.append({"plan":phase["desc"],"reason":phase["reason"],"answer":result["reflection"]})

        if self.result_validate(problem, current_trajectory):
            pass
        else:
            current_trajectory.append(self.inference_final(problem, current_trajectory))
        return {"current_trajectory": current_trajectory}
    
    
    async def di_run(self, problem, current_trajectory, subgoal):
        print("run di_run")
        DI = DataInterpreter()
        record = await DI.run(di_prompt.format(problem_desc=problem, trajectory=current_trajectory, subgoal=subgoal))
        return record.content
    
    def inference(self, problem, current_trajectory, subgoal):
        print("run inference")
        inference_result = self.llm.llm_response(prompt=inference_prompt.format(problem_desc=problem, trajectory=current_trajectory),json_mode=True)
        return inference_result
    
    def logic_validate(self, problem, current_trajectory, subgoal):
        print("run logic validate")
        validate_result = self.llm.llm_response(prompt=logic_validate_prompt.format(problem_desc=problem, trajectory=current_trajectory, subgoal = subgoal),json_mode=True)
        return validate_result
    
    def result_validate(self, problem, current_trajectory):
        result_validate_result = self.llm.llm_response(prompt=result_validate_prompt.format(problem_desc=problem, trajectory=current_trajectory),json_mode=True)
        return result_validate_result
    
    def inference_final(self, problem, current_trajectory):
        final_result = self.llm.llm_response(prompt=inference_final_prompt.format(problem_desc=problem, trajectory=current_trajectory))
        return final_result
    
