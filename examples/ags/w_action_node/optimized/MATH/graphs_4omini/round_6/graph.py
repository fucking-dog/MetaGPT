from typing import Literal
import examples.ags.w_action_node.optimized.MATH.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.MATH.graphs.round_6.prompt as prompt_custom
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
        code_solutions = []
        for _ in range(3):  # Generate 3 solutions
            code_solution = await self.programmer(problem=problem)
            code_solutions.append(code_solution['code'] + '\n' + code_solution['output'])

        ensemble_result = await self.sc_ensemble(solutions=code_solutions, problem=problem)
        
        # Add verification step
        verification = await self.custom(input=problem + f"\nEnsemble result:\n{ensemble_result['response']}", instruction=prompt_custom.VERIFY_ENSEMBLE_PROMPT)
        
        if verification['response'].lower().startswith('correct'):
            refined_solution = await self.custom(input=problem + f"\nEnsemble result:\n{ensemble_result['response']}", instruction=prompt_custom.REFINE_SOLUTION_PROMPT)
        else:
            corrected_solution = await self.custom(input=problem + f"\nEnsemble result:\n{ensemble_result['response']}\nVerification result:\n{verification['response']}", instruction=prompt_custom.CORRECT_SOLUTION_PROMPT)
            refined_solution = await self.custom(input=problem + f"\nCorrected solution:\n{corrected_solution['response']}", instruction=prompt_custom.REFINE_SOLUTION_PROMPT)
        
        final_verification = await self.custom(input=problem + f"\nRefined solution:\n{refined_solution['response']}", instruction=prompt_custom.VERIFY_SOLUTION_PROMPT)
        
        if final_verification['response'].lower().startswith('correct'):
            return refined_solution['response'], self.llm.cost_manager.total_cost
        else:
            final_correction = await self.custom(input=problem + f"\nRefined solution:\n{refined_solution['response']}\nVerification result:\n{final_verification['response']}", instruction=prompt_custom.CORRECT_SOLUTION_PROMPT)
            return final_correction['response'], self.llm.cost_manager.total_cost
                    