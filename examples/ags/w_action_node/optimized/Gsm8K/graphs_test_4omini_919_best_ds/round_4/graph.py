from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_4.prompt as prompt_custom
from metagpt.provider.llm_provider_registry import create_llm_instance
from metagpt.utils.cost_manager import CostManager

DatasetType = Literal["HumanEval", "MMBP", "Gsm8K", "MATH", "HotpotQa", "MMLU"]

import re

class SolveGraph:
    def __init__(
        self,
        name: str,
        llm_config,
        dataset: DatasetType,
    ) -> None:
        self.name = name
        self.dataset = dataset
        self.llm = create_llm_instance(llm_config)
        self.llm.cost_manager = CostManager()
        self.custom = operator.Custom(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        solution = await self.custom(input=problem, instruction=prompt_custom.SOLVE_PROMPT)
        review = await self.custom(input=f"Problem: {problem}\nSolution: {solution['response']}", instruction=prompt_custom.REVIEW_PROMPT)
        final_solution = review['response']
        
        # Extract numerical answer
        try:
            match = re.search(r'\$?(\d+(\.\d+)?)', final_solution)
            if match:
                numerical_answer = float(match.group(1))
            else:
                numerical_answer = None
        except ValueError:
            numerical_answer = None

        return final_solution, numerical_answer, self.llm.cost_manager.total_cost
                    