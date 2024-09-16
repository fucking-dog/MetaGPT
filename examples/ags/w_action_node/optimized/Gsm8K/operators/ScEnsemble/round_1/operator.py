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
from examples.ags.w_action_node.optimized.Gsm8K.operators.ScEnsemble.round_1.prompt import *

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
        node = await ActionNode.from_pydantic(ScEnsembleOp).fill(context=prompt, llm=self.llm, mode="context_fill")
        response = node.instruct_content.model_dump()

        answer = response.get("solution_letter", "")
        answer = answer.strip().upper()

        return {"response": solutions[answer_mapping[answer]]}  # {"final_solution": "xxx"}
                    