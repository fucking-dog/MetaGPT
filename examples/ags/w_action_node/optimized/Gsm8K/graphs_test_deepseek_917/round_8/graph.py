from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_8.prompt as prompt_custom
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.prompt_lib as prompt_lib
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
        self.format = operator.Format(self.llm)
        self.custom = operator.Custom(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        approaches = ["algebraic", "geometric", "numerical"]
        all_solutions = []
        for approach in approaches:
            for prompt in [prompt_custom.SOLVE_PROMPT_1, prompt_custom.SOLVE_PROMPT_2]:
                solution = await self.custom(input=f"Problem: {problem}\nApproach: {approach}", instruction=prompt)
                all_solutions.append(solution['response'])
        
        best_solution = await self.custom(input=f"Problem: {problem}\nSolutions: {all_solutions}", instruction=prompt_custom.SELECT_BEST_PROMPT)
        
        reviewed_solution = await self.custom(input=f"Problem: {problem}\nInitial Solution: {best_solution['response']}", instruction=prompt_custom.REVIEW_PROMPT)
        refined_solution = await self.custom(input=f"Problem: {problem}\nReviewed Solution: {reviewed_solution['response']}", instruction=prompt_custom.REFINE_PROMPT)
        format_solution = await self.format(problem=problem, solution=refined_solution['response'])
        return format_solution['response'], self.llm.cost_manager.total_cost
                    