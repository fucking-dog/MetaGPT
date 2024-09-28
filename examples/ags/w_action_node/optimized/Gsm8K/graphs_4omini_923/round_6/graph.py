from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_6.prompt as prompt_custom
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
        self.sc_ensemble = operator.ScEnsemble(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        solutions = []
        for _ in range(3):  # Generate 3 solutions
            initial_solution = await self.custom(input=problem, instruction=prompt_custom.SOLVE_PROMPT)
            solutions.append(initial_solution['response'])
        
        ensemble_result = await self.sc_ensemble(solutions=solutions, problem=problem)
        
        review_instruction = f"Review and verify the following solution:\n{ensemble_result['response']}\nProblem: {problem}"
        reviewed_solution = await self.programmer(problem=review_instruction)
        
        if reviewed_solution['output']:
            correction_instruction = f"The original solution might have errors. Please provide a corrected solution with detailed steps:\n{reviewed_solution['output']}\nOriginal problem: {problem}"
            corrected_solution = await self.custom(input=correction_instruction, instruction=prompt_custom.CORRECTION_PROMPT)
            final_solution = corrected_solution['response']
        else:
            final_solution = ensemble_result['response']
        
        return final_solution, self.llm.cost_manager.total_cost
                    