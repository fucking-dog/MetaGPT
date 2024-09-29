from typing import Literal
import examples.ags.w_action_node.optimized.MATH.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.MATH.graphs.round_8.prompt as prompt_custom
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

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        # Generate multiple solutions using different approaches
        solutions = []
        for approach in ["step_by_step", "visual", "algebraic"]:
            solution = await self.custom(input=problem, instruction=prompt_custom.SOLVE_PROMPT.format(approach=approach))
            solutions.append(solution['response'])

        # Select the best solution using ScEnsemble
        best_solution = await self.sc_ensemble(solutions=solutions, problem=problem)

        # Review and potentially improve the solution
        reviewed_solution = await self.custom(input=f"Problem: {problem}\nCurrent solution: {best_solution['response']}", instruction=prompt_custom.REVIEW_PROMPT)

        # Verify the final solution
        verified_solution = await self.custom(input=f"Problem: {problem}\nFinal solution: {reviewed_solution['response']}", instruction=prompt_custom.VERIFY_PROMPT)

        return verified_solution['response'], self.llm.cost_manager.total_cost
                    