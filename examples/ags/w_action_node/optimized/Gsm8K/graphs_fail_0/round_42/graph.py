from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_42.prompt as prompt_custom
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
        self.generate = operator.Generate(self.llm)
        self.format = operator.Format(self.llm)
        self.custom = operator.Custom(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        initial_solution = await self.custom(input=problem, instruction=prompt_custom.INITIAL_SOLUTION_PROMPT)
        
        # Self-review step
        review_result = await self.custom(input=f"Problem: {problem}\nSolution: {initial_solution['response']}", instruction=prompt_custom.SELF_REVIEW_PROMPT)
        
        if "error" in review_result['response'].lower() or "incorrect" in review_result['response'].lower():
            corrected_solution = await self.custom(input=f"Problem: {problem}\nInitial Solution: {initial_solution['response']}\nReview: {review_result['response']}", instruction=prompt_custom.CORRECTION_PROMPT)
            final_solution = corrected_solution['response']
        else:
            final_solution = initial_solution['response']
        
        format_solution = await self.format(problem=problem, solution=final_solution)
        return format_solution, self.llm.cost_manager.total_cost
                    