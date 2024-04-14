# -*- coding: utf-8 -*-
# Date       : 2023/4/3
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: run math ai

import asyncio
from math_ai.codebase.gate_controller import GateController
from math_ai.codebase.math_resovler import MathResolver
from math_ai.codebase.data_processer import DataProcesser
from math_ai.codebase.solution_refiner import SolutionRefiner


async def solution(question_path: str):
    final_solutions = []
    idx = 1

    dp = DataProcesser()
    gc = GateController()
    mr = MathResolver()
    sr = SolutionRefiner()


    problem_dict_list = dp.run(question_path)  # List[Dict]
    for problem_dict in problem_dict_list:
        strategy_dict = gc.run(problem_dict)
        first_solution = await mr.single_run(problem_dict, strategy_dict)  # 使用 await
        final_solution = sr.run(problem_dict, strategy_dict, first_solution)

        print(problem_dict)
        print("\n\n\n")
        print(final_solution)

        # 写入结果
        with open(f'result/{idx}.txt', 'w') as file:
            idx += 1
            file.write(final_solution)
        final_solutions.append(final_solution)

    return final_solutions

async def main(question_path: str):
    solutions = await solution(question_path)
    print(solutions)

if __name__ == '__main__':
    question_path = './math_ai/dataset/2024.json'
    asyncio.run(main(question_path))