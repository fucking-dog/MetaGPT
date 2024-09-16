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
from examples.ags.w_action_node.optimized.Gsm8K.operators.Review.round_3.prompt import *

class Review(Operator):
    def __init__(self, llm: LLM, criteria: str = "accuracy", name: str = "Review"):
        self.criteria = criteria
        super().__init__(name, llm)

    async def __call__(self, problem, solution):
        prompt = REVIEW_PROMPT.format(problem=problem, solution=solution, criteria=self.criteria)
        node = await ActionNode.from_pydantic(ReviewOp).fill(context=prompt, llm=self.llm, mode="context_fill")
        response = node.instruct_content.model_dump()
        return response  # {"review_result": True, "feedback": "xxx"}
                    