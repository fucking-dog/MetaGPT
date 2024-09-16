from typing import Literal, List, Dict, Tuple
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt
import random
from collections import Counter
from metagpt.llm import LLM
from metagpt.provider.llm_provider_registry import create_llm_instance
from examples.ags.w_action_node.operator import Operator
from metagpt.actions.action_node import ActionNode
from examples.ags.w_action_node.optimized.Gsm8K.operators.template.operator_an import *
from examples.ags.w_action_node.optimized.Gsm8K.operators.Revise.round_4.prompt import *

class Revise(Operator):
    def __init__(self, llm: LLM, name: str = "Revise"):
        super().__init__(name, llm)

    async def __call__(self, problem, solution, feedback):
        prompt = REVISE_PROMPT.format(problem=problem, solution=solution, feedback=feedback)
        node = await ActionNode.from_pydantic(ReviseOp).fill(context=prompt, llm=self.llm, mode="single_fill")
        response = node.instruct_content.model_dump()
        return response  # {"solution": "xxx"}
                    