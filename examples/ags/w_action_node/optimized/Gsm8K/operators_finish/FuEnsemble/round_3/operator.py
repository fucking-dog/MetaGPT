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
from examples.ags.w_action_node.optimized.Gsm8K.operators.FuEnsemble.round_3.prompt import *

class FuEnsemble(Operator):
    """
    Function: Critically evaluating multiple solution candidates, synthesizing their strengths, and developing an enhanced, integrated solution.
    """

    def __init__(self, llm: LLM, name: str = "FuEnsemble"):
        super().__init__(name, llm)

    async def __call__(self, solutions: List, problem):
        solution_text = ""
        for solution in solutions:
            solution_text += str(solution) + "\n"
        prompt = FU_ENSEMBLE_PROMPT.format(solutions=solution_text, problem=problem)
        node = await ActionNode.from_pydantic(FuEnsembleOp).fill(context=prompt, llm=self.llm, mode="context_fill")
        response = node.instruct_content.model_dump()
        return {"solution": response["final_solution"]}  # {"final_solution": "xxx"}
                    