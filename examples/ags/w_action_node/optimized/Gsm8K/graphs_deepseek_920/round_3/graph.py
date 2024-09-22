from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_3.prompt as prompt_custom
from metagpt.provider.llm_provider_registry import create_llm_instance
from metagpt.utils.cost_manager import CostManager

DatasetType = Literal["HumanEval", "MMBP", "Gsm8K", "MATH", "HotpotQa", "MMLU"]

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
        self.programmer = operator.Programmer(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        solution = await self.custom(input=problem, instruction=prompt_custom.SOLVE_PROMPT)
        analysis = f"The problem: {problem}\nThe solution: {solution['response']}"
        verification = await self.programmer(problem=analysis, analysis="Verify the extracted answer and correct it if necessary.")
        review = await self.custom(input=f"{problem}\n{solution['response']}\n{verification['output']}", instruction=prompt_custom.REVIEW_PROMPT)
        final_answer = await self.programmer(problem=review['response'], analysis="Extract the final numerical answer from the review.")
        return final_answer['output'], self.llm.cost_manager.total_cost
                    