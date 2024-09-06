# -*- coding: utf-8 -*-
# @Date    : 6/27/2024 17:36 PM
# @Author  : didi
# @Desc    : operator demo of ags
import random
from collections import Counter
from typing import Dict, List, Tuple

from tenacity import retry, stop_after_attempt

from examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator_an import *
from examples.ags.w_action_node.optimized.Gsm8K.graphs.template.op_prompt import *
from metagpt.actions.action_node import ActionNode
from metagpt.llm import LLM


class Operator:
    def __init__(self, name, llm: LLM):
        self.name = name
        self.llm = llm

    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class Generate(Operator):
    def __init__(self, llm: LLM, name: str = "Generate"):
        super().__init__(name, llm)

    async def __call__(self, input, prompt):
        prompt = prompt + input
        node = await ActionNode.from_pydantic(GenerateOp).fill(context=prompt, llm=self.llm, mode="single_fill", schema='raw')
        response = node.instruct_content.model_dump()
        return response


class Format(Operator):
    def __init__(self, llm: LLM, name: str = "Format"):
        super().__init__(name, llm)

    async def __call__(self, input):
        prompt = FORMAT_PROMPT.format(input=input)
        node = await ActionNode.from_pydantic(GenerateOp).fill(context=prompt, llm=self.llm, mode="single_fill", schema='raw')
        response = node.instruct_content.model_dump()
        return response
