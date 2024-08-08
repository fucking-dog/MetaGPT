# -*- coding: utf-8 -*-
# @Date    : 6/27/2024 22:07 PM
# @Author  : didi
# @Desc    : graph & an instance - humanevalgraph

from metagpt.llm import LLM 
from typing import List
from examples.ags.w_action_node.operator import Generate, GenerateCode, GenerateCodeBlock, Review, Revise, FuEnsemble, MdEnsemble, DbEnsemble, GenerateOnContext, Format
from examples.ags.w_action_node.utils import get_hotpotqa

class Graph:
    def __init__(self, name:str, llm:LLM) -> None:
        self.name = name
        self.model = llm 

    def __call__():
        NotImplementedError("Subclasses must implement __call__ method")

    def optimize(dataset:List):
        pass

class HumanEvalGraph(Graph):
    def __init__(self, name:str, llm: LLM, criteria:str, vote_count:int = 10) -> None:
        super().__init__(name, llm)
        self.criteria = criteria # TODO 自动构建图时，图的初始参数与图所使用的算子要求的外部参数相匹配
        self.generate_code = GenerateCode(llm=llm)
        self.generate_code_block = GenerateCodeBlock(llm=llm)
        self.review = Review(llm=llm, criteria=criteria)
        self.revise = Revise(llm=llm)
        self.fuensemble = FuEnsemble(llm=llm)
        self.mdensemble = MdEnsemble(llm=llm, vote_count=vote_count)

    async def __call__(self, case_id:str, problem:str, ensemble_count:int = 5):
        solution_list = []
        for _ in range(ensemble_count):
            for retry_count in range(5):
                try:
                    # solution = await self.generate_code(problem)
                    solution = await self.generate_code_block(problem)
                    solution = solution.get('code_solution')
                    solution_list.append(solution)
                    break
                except Exception as e:
                    print(e)
            # solution list 有5个
        solution = await self.mdensemble(case_id, "code", solution_list, problem)
        return solution
    
    async def review_revise_ensemble(self, problem:str, ensemble_count:int = 2):
        solution_list = []
        for _ in range(ensemble_count):
            solution = await self.single_solve(problem, 3)
            solution_list.append(solution)
        solution = await self.ensemble(solution_list, problem)
        return solution

    # async def simple_ensemble(self, problem:str, ensemble_count:int = 3):
    # async def __call__(self, problem:str, ensemble_count:int = 3):
    #     solution_list = []
    #     for _ in range(ensemble_count):
    #         solution = await self.generate_code(problem)
    #         # solution = await self.generate_code_block(problem)
    #         solution = solution.get('code_solution')
    #         solution_list.append(solution)
    #     solution = await self.fuensemble(solution_list, problem)
    #     return solution
    
    async def single_solve(self, problem:str, max_loop:int):
        solution = await self.generate_code(problem)
        solution = solution.get('code_solution')
        for _ in range(max_loop):
            review_feedback = await self.review(problem, solution)
            if review_feedback['review_result']:
                break
            solution = await self.revise(problem, solution, review_feedback['feedback'])
            solution = solution.get('revised_solution')
        return solution
    
class HotpotQAGraph(Graph):
    def __init__(self, name:str, llm:LLM, criteria:str ,HOTPOTQA_PATH:str) -> None:
        super().__init__(name, llm)
        self.generate_on_context = GenerateOnContext(llm=llm)
        self.format = Format(llm=llm)
        self.review = Review(llm=llm, criteria=criteria)
        self.revise = Revise(llm=llm)
        self.hotpotqa_path = HOTPOTQA_PATH

    async def __call__(self, id:str, max_loop:int = 1):
        dp = get_hotpotqa(self.hotpotqa_path)[id]
        paragraphs = [item[1] for item in dp['context'] if isinstance(item[1], list)]
        context_str = "\n".join(" ".join(paragraph) for paragraph in paragraphs)

        answer_result = await self.generate_on_context(dp['question'], context_str)
        answer_result = answer_result.get("solution")
        
        for _ in range(max_loop):
            review_result = await self.review(dp['question'], answer_result)
            if review_result['review_result']:
                break
            answer_result = await self.revise(dp['question'], answer_result, review_result['feedback'])
            answer_result = answer_result.get('revised_solution')

        answer_formated = await self.format(dp['question'], answer_result)

        sample_dict = dict(task_id=id, answer=answer_formated.get("solution"))
        return sample_dict
    

class Gsm8kGraph(Graph):
    pass