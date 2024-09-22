from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_3.prompt as prompt_custom
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
        solutions = []
        for _ in range(3):
            solution = await self.custom(input=problem, instruction=prompt_custom.SOLVE_PROMPT)
            solutions.append(solution['response'])
        
        best_solution = await self.custom(input=f"Problem: {problem}\nSolutions: {solutions}", instruction=prompt_custom.SELECT_BEST_PROMPT)
        
        reviewed_solution = await self.custom(input=f"Problem: {problem}\nInitial Solution: {best_solution['response']}", instruction=prompt_custom.REVIEW_PROMPT)
        format_solution = await self.format(problem=problem, solution=reviewed_solution['response'])
        return format_solution['response'], self.llm.cost_manager.total_cost
                    