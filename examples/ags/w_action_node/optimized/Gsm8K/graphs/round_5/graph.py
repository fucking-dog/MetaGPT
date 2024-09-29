from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_5.prompt as prompt_custom
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
        
        review_result = await self.programmer(problem=problem, analysis=final_solution['response'])
        
        if review_result['output']:
            initial_answer = review_result['output']
        else:
            initial_answer = final_solution['response']
        
        # Add a final check and correction step
        final_check = await self.custom(input=f"Problem: {problem}\nInitial Answer: {initial_answer}", instruction=prompt_custom.FINAL_CHECK_PROMPT)
        
        return final_check['response'], self.llm.cost_manager.total_cost
                    