from typing import Literal
import examples.ags.w_action_node.optimized.MATH.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.MATH.graphs.round_3.prompt as prompt_custom
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
        # Generate initial solution
        initial_solution = await self.custom(input=problem, instruction=prompt_custom.INITIAL_SOLUTION_PROMPT)
        
        # Generate multiple solutions using ScEnsemble
        solutions = []
        for _ in range(3):
            solution = await self.custom(input=problem + f"\nInitial solution: {initial_solution['response']}", instruction=prompt_custom.GENERATE_SOLUTION_PROMPT)
            solutions.append(solution['response'])
        
        # Use ScEnsemble to select the most consistent solution
        final_solution = await self.sc_ensemble(solutions=solutions, problem=problem)
        
        return final_solution['response'], self.llm.cost_manager.total_cost
                    