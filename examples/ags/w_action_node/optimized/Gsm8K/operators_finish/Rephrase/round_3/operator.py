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
from examples.ags.w_action_node.optimized.Gsm8K.operators.Rephrase.round_3.prompt import *

class Rephrase(Operator):
    """
    Paper: Code Generation with AlphaCodium: From Prompt Engineering to Flow Engineering
    Link: https://arxiv.org/abs/2404.14963
    Paper: Achieving >97% on GSM8K: Deeply Understanding the Problems Makes LLMs Better Solvers for Math Word Problems
    Link: https://arxiv.org/abs/2404.14963
    """

    def __init__(self, llm: LLM, name: str = "Rephrase"):
        super().__init__(name, llm)

    async def __call__(self, problem: str) -> str:
        prompt = REPHRASE_PROMPT.format(problem=problem)
        node = await ActionNode.from_pydantic(RephraseOp).fill(context=prompt, llm=self.llm, mode="single_fill")
        response = node.instruct_content.model_dump()
        return response  # {"rephrased_problem": "xxx"}
                    