from typing import Literal
import examples.ags.w_action_node.optimized.MATH.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.MATH.graphs.round_11.prompt as prompt_custom
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
        # Generate multiple solutions using different approaches
        solutions = []
        for i in range(3):
            solution = await self.custom(input=problem, instruction=prompt_custom.GENERATE_SOLUTION_PROMPT.format(approach=i+1))
            solutions.append(solution['response'])

        # Use programmer to generate a code-based solution
        code_solution = await self.programmer(problem=problem)
        solutions.append(code_solution['code'] + '\n' + code_solution['output'])

        # Ensemble the solutions
        ensemble_result = await self.sc_ensemble(solutions=solutions, problem=problem)
        
        # Verify mathematical correctness
        verified_result = await self.custom(input=problem + f"\nEnsemble result:\n{ensemble_result['response']}", instruction=prompt_custom.VERIFY_MATH_CORRECTNESS_PROMPT)
        
        # Refine the solution
        refined_solution = await self.custom(input=problem + f"\nVerified result:\n{verified_result['response']}", instruction=prompt_custom.REFINE_SOLUTION_PROMPT)
        
        # Final verification and formatting
        verified_solution = await self.custom(input=problem + f"\nRefined solution:\n{refined_solution['response']}", instruction=prompt_custom.VERIFY_SOLUTION_PROMPT)
        final_solution = await self.custom(input=problem + f"\nVerified solution:\n{verified_solution['response']}", instruction=prompt_custom.SIMPLIFY_AND_FORMAT_PROMPT)
        
        return final_solution['response'], self.llm.cost_manager.total_cost
                    