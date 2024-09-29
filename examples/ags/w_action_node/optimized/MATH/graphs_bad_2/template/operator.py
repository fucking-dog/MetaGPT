# -*- coding: utf-8 -*-
# @Date    : 6/27/2024 17:36 PM
# @Author  : didi
# @Desc    : operator demo of ags
import ast
import random
import sys
import traceback
from collections import Counter
from typing import Dict, List, Tuple

from tenacity import retry, stop_after_attempt, wait_fixed

from examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator_an import *
from examples.ags.w_action_node.optimized.Gsm8K.graphs.template.op_prompt import *
from examples.ags.w_action_node.utils import test_case_2_test_function
from metagpt.actions.action_node import ActionNode
from metagpt.llm import LLM
from metagpt.logs import logger
import re
import asyncio


class Operator:
    def __init__(self, name, llm: LLM):
        self.name = name
        self.llm = llm

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class Custom(Operator):
    def __init__(self, llm: LLM, name: str = "Custom"):
        super().__init__(name, llm)

    async def __call__(self, input, instruction):
        prompt = instruction + input
        node = await ActionNode.from_pydantic(GenerateOp).fill(context=prompt, llm=self.llm, mode="single_fill")
        response = node.instruct_content.model_dump()
        return response


class Programmer(Operator):
    def __init__(self, llm: LLM, name: str = "Programmer"):
        super().__init__(name, llm)

    async def exec_code(self, code, timeout=60):
        try:
            # 预先导入数学相关的包
            global_namespace = {
                "__builtins__": __builtins__,
                "math": __import__("math"),
                "numpy": __import__("numpy"),
                "pandas": __import__("pandas"),
                "re": __import__("re"),
                "random": __import__("random"),
                # 根据需要添加更多预先导入的包
            }

            # 定义一个内部函数来执行代码
            def run_exec():
                exec(code, global_namespace)
                if 'solve' in global_namespace:
                    return global_namespace['solve']()
                else:
                    raise ValueError("未找到'solve'函数")

            # 获取当前事件循环
            loop = asyncio.get_event_loop()
            # 使用 run_in_executor 在默认的线程池中执行代码，并应用超时
            result = await asyncio.wait_for(loop.run_in_executor(None, run_exec), timeout=timeout)
            return "Success", str(result)

        except asyncio.TimeoutError:
            return "Error", f"执行超时，超过了{timeout}秒"
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
            return "Error", f"执行错误: {str(e)}\n{''.join(tb_str)}"

    async def code_generate(self, problem, analysis, feedback, mode):
        prompt = PYTHON_CODE_VERIFIER_PROMPT.format(problem=problem, analysis=analysis, feedback=feedback)
        fill_kwargs = {"context": prompt, "llm": self.llm, "function_name": "solve"}
        if mode:
            fill_kwargs["mode"] = mode
        node = await ActionNode.from_pydantic(CodeGenerateOp).fill(**fill_kwargs)
        response = node.instruct_content.model_dump()
        return response

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def __call__(self, problem: str, analysis: str = "None"):
        code = None
        output = None
        feedback = ""
        for i in range(3):
            code_response = await self.code_generate(problem, analysis, feedback, mode="code_fill")
            code = code_response.get("code")
            if not code:
                return {"code": code, "output": "未生成代码"}

            status, output = await self.exec_code(code)
            if status == "Success":
                return {"code": code, "output": output}
            else:
                print(f"第{i + 1}次执行错误，错误信息：{output}")
                feedback = (
                    f"\nThe result of the error from the code you wrote in the previous round:\n"
                    f"Code:{code}\n\nStatus:{status},{output}"
                )
        return {"code": code, "output": output}


class ScEnsemble(Operator):
    """
    Paper: Self-Consistency Improves Chain of Thought Reasoning in Language Models
    Link: https://arxiv.org/abs/2203.11171
    Paper: Universal Self-Consistency for Large Language Model Generation
    Link: https://arxiv.org/abs/2311.17311
    """

    def __init__(self,llm: LLM , name: str = "ScEnsemble"):
        super().__init__(name, llm)

    async def __call__(self, solutions: List[str], problem: str):
        answer_mapping = {}
        solution_text = ""
        for index, solution in enumerate(solutions):
            answer_mapping[chr(65 + index)] = index
            solution_text += f"{chr(65 + index)}: \n{str(solution)}\n\n\n"

        prompt = SC_ENSEMBLE_PROMPT.format(solutions=solution_text, problem=problem)
        node = await ActionNode.from_pydantic(ScEnsembleOp).fill(context=prompt, llm=self.llm)
        response = node.instruct_content.model_dump()

        answer = response.get("solution_letter", "")
        answer = answer.strip().upper()

        return {"response": solutions[answer_mapping[answer]]}
