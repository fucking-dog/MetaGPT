# -*- coding: utf-8 -*-
# @Date    : 6/27/2024 17:36 PM
# @Author  : didi
# @Desc    : operator demo of ags
import ast
import builtins
import concurrent
import random
import sys
import traceback
from collections import Counter
from typing import Dict, List, Tuple, Any

from tenacity import stop_after_attempt, wait_fixed

from examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator_an import *
from examples.ags.w_action_node.optimized.Gsm8K.graphs.template.op_prompt import *
from examples.ags.w_action_node.utils import test_case_2_test_function
from metagpt.actions.action_node import ActionNode
from metagpt.llm import LLM
from metagpt.logs import logger
import re
import logging

import asyncio
import concurrent.futures
import sys
import traceback
import builtins
from typing import Dict, Any, Tuple
import logging
from retrying import retry

# 配置日志
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# 顶层函数，避免本地函数无法序列化的问题
def run_code(code: str) -> Tuple[str, str]:
    try:
        logging.debug("开始执行用户代码")
        # 设置递归深度限制
        sys.setrecursionlimit(1000)  # 根据需要调整

        allowed_modules = {
            "math": __import__("math"),
            "numpy": __import__("numpy"),
            "pandas": __import__("pandas"),
            "re": __import__("re"),
            "random": __import__("random"),
        }

        global_namespace: Dict[str, Any] = {
            "__builtins__": builtins,
            **allowed_modules
        }

        # 禁止的库列表，包括 'multiprocessing' 等
        disallowed_imports = [
            "os", "sys", "subprocess", "multiprocessing",
            "matplotlib", "seaborn", "plotly", "bokeh", "ggplot",
            "pylab", "tkinter", "PyQt5", "wx", "pyglet"
        ]

        # 检查禁止导入的库
        for lib in disallowed_imports:
            if f"import {lib}" in code or f"from {lib}" in code:
                logging.warning("检测到禁止导入的库: %s", lib)
                return "Error", f"禁止导入的库: {lib}"

        # 使用exec执行代码
        exec(code, global_namespace)

        # 假设代码中定义了一个名为'solve'的函数
        if 'solve' in global_namespace:
            result = global_namespace['solve']()
            logging.debug("用户代码执行成功，结果: %s", result)
            return "Success", str(result)
        else:
            logging.warning("未找到'solve'函数")
            return "Error", "未找到'solve'函数"

    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        logging.error("执行代码时发生异常: %s\n%s", e, tb_str)
        return "Error", f"执行错误: {str(e)}\n{tb_str}"


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
    def __init__(self, llm: Any, name: str = "Programmer"):
        super().__init__(name, llm)

    @staticmethod
    async def exec_code(code: str, timeout: int = 10) -> Tuple[str, str]:
        try:
            result = await asyncio.wait_for(asyncio.to_thread(run_code, code), timeout=timeout)
            return result
        except asyncio.TimeoutError:
            logging.error("代码执行超时")
            return "Error", "代码执行超时"

    async def code_generate(self, problem: str, analysis: str, feedback: str, mode: str):
        # 假设 PYTHON_CODE_VERIFIER_PROMPT 和 ActionNode 已正确定义
        prompt = PYTHON_CODE_VERIFIER_PROMPT.format(problem=problem, analysis=analysis, feedback=feedback)
        fill_kwargs = {"context": prompt, "llm": self.llm, "function_name": "solve"}
        if mode:
            fill_kwargs["mode"] = mode
        node = await ActionNode.from_pydantic(CodeGenerateOp).fill(**fill_kwargs)
        response = node.instruct_content.model_dump()
        return response

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def __call__(self, problem: str, analysis: str = "None") -> Dict[str, str]:
        code = None
        feedback = ""
        for i in range(3):
            code_response = await self.code_generate(problem, analysis, feedback, mode="code_fill")
            code = code_response["code"]
            status, output = await self.exec_code(code)
            if status == "Success":
                return {"code": code, "output": output}
            else:
                logging.warning("第%d次执行错误，错误信息：%s", i + 1, output)
                feedback = f"\nThe result of the error from the code you wrote in the previous round:\nCode:{code}\n\nStatus:{status},{output}"
        return {"code": code, "output": "error"}



class ScEnsemble(Operator):
    """
    Paper: Self-Consistency Improves Chain of Thought Reasoning in Language Models
    Link: https://arxiv.org/abs/2203.11171
    Paper: Universal Self-Consistency for Large Language Model Generation
    Link: https://arxiv.org/abs/2311.17311
    """

    def __init__(self, llm: LLM, name: str = "ScEnsemble"):
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
