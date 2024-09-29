from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_22.prompt as prompt_custom
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
        self.sc_ensemble = operator.ScEnsemble(self.llm)
        self.programmer = operator.Programmer(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        solutions = []
        for _ in range(3):
            solution = await self.custom(input=problem, instruction=prompt_custom.MATH_SOLVE_PROMPT)
            solutions.append(solution['response'])
        
        final_solution = await self.sc_ensemble(solutions=solutions, problem=problem)
        
        # Add a verification step using the Programmer operator
        review_result = await self.programmer(problem=problem, analysis=final_solution['response'])
        
        # Add a final review step using the Custom operator
        final_review = await self.custom(input=f"Problem: {problem}\nCalculated answer: {review_result['output']}", instruction=prompt_custom.FINAL_REVIEW_PROMPT)
        
        return final_review['response'], self.llm.cost_manager.total_cost
                    