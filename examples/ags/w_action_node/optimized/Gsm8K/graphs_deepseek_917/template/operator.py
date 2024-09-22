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

from tenacity import retry, stop_after_attempt

from examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator_an import *
from examples.ags.w_action_node.optimized.Gsm8K.graphs.template.op_prompt import *
from examples.ags.w_action_node.utils import test_case_2_test_function
from metagpt.actions.action_node import ActionNode
from metagpt.llm import LLM
from metagpt.logs import logger


class Operator:
    def __init__(self, name, llm: LLM):
        self.name = name
        self.llm = llm

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

class Format(Operator):
    def __init__(self,llm: LLM, name: str = "Format"):
        super().__init__(name, llm)

    # 使用JSON MODE 输出 Formatted 的结果
    async def __call__(self, problem, solution):
        prompt = FORMAT_PROMPT.format(problem=problem, solution=solution)
        node = await ActionNode.from_pydantic(FormatOp).fill(context=prompt, llm=self.llm, mode="single_fill")
        response = node.instruct_content.model_dump()
        return response  # {"solution":"xxx"}


class Custom(Operator):
    def __init__(self, llm: LLM, name: str = "Custom"):
        super().__init__(name, llm)

    async def __call__(self, input, instruction):
        prompt = input + instruction
        node = await ActionNode.from_pydantic(GenerateOp).fill(context=prompt, llm=self.llm, mode="single_fill")
        response = node.instruct_content.model_dump()
        return response
