from typing import Literal
import examples.ags.w_action_node.optimized.MATH.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.MATH.graphs.round_25.prompt as prompt_custom
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
        
        verified_result = await self.custom(input=problem + f"\nEnsemble result:\n{ensemble_result['response']}", instruction=prompt_custom.VERIFY_MATH_CORRECTNESS_PROMPT)
        
        refined_solution = await self.custom(input=problem + f"\nVerified result:\n{verified_result['response']}", instruction=prompt_custom.REFINE_SOLUTION_PROMPT)
        verified_solution = await self.custom(input=problem + f"\nRefined solution:\n{refined_solution['response']}", instruction=prompt_custom.VERIFY_SOLUTION_PROMPT)
        simplified_solution = await self.custom(input=problem + f"\nVerified solution:\n{verified_solution['response']}", instruction=prompt_custom.SIMPLIFY_AND_FORMAT_PROMPT)
        
        # Add final check and correction step
        final_solution = await self.custom(input=problem + f"\nSimplified solution:\n{simplified_solution['response']}", instruction=prompt_custom.FINAL_CHECK_AND_CORRECT_PROMPT)
        
        return final_solution['response'], self.llm.cost_manager.total_cost
                    