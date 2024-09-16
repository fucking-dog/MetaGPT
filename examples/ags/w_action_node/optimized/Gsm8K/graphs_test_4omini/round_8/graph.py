from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_8.prompt as prompt_custom
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
        self.sc_ensemble = operator.ScEnsemble(self.llm)
        self.custom = operator.Custom(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        solutions = []
        for _ in range(3):  # Generate 3 solutions
            solution = await self.generate(problem=problem)
            solutions.append(solution['response'])
        
        best_solution = await self.sc_ensemble(solutions=solutions, problem=problem)
        
        # Add self-consistency check
        consistency_check = await self.custom(input=f"Problem: {problem}\nSolution: {best_solution['response']}", instruction=prompt_custom.CONSISTENCY_CHECK_PROMPT)
        
        if consistency_check['response'].lower() == 'consistent':
            # Add simplification step
            simplified_solution = await self.custom(input=f"Problem: {problem}\nSolution: {best_solution['response']}", instruction=prompt_custom.SIMPLIFY_SOLUTION_PROMPT)
            format_solution = await self.format(problem=problem, solution=simplified_solution['response'])
            return format_solution['response'], self.llm.cost_manager.total_cost
        else:
            # If not consistent, generate a new solution
            new_solution = await self.generate(problem=problem)
            # Simplify the new solution as well
            simplified_new_solution = await self.custom(input=f"Problem: {problem}\nSolution: {new_solution['response']}", instruction=prompt_custom.SIMPLIFY_SOLUTION_PROMPT)
            format_solution = await self.format(problem=problem, solution=simplified_new_solution['response'])
            return format_solution['response'], self.llm.cost_manager.total_cost
                    