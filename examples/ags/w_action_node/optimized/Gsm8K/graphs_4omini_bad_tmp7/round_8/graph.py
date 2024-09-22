from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_8.prompt as prompt_custom
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
        initial_solution = await self.custom(input=problem, instruction=prompt_custom.SOLVE_PROMPT)
        
        calculation_request = f"Problem: {problem}\nInitial solution: {initial_solution['response']}\nPerform any necessary calculations and return the final numerical answer."
        
        calculated_solution = await self.programmer(problem=calculation_request)
        
        review_request = f"Problem: {problem}\nCalculated solution: {calculated_solution['output']}\nInitial solution: {initial_solution['response']}"
        reviewed_solution = await self.custom(input=review_request, instruction=prompt_custom.REVIEW_PROMPT)
        
        final_answer = reviewed_solution['response'].strip()
        
        return final_answer, self.llm.cost_manager.total_cost
                    