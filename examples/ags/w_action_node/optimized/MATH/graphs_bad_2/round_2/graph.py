from typing import Literal
import examples.ags.w_action_node.optimized.MATH.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.MATH.graphs.round_2.prompt as prompt_custom
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
            try:
                solution = await self.custom(input=problem, instruction=prompt_custom.MATH_SOLVE_PROMPT)
                solutions.append(solution['response'])
            except Exception as e:
                print(f"Error in Custom operator: {e}")
                continue

        if not solutions:
            return "Unable to generate a solution.", self.llm.cost_manager.total_cost

        ensemble_result = await self.sc_ensemble(solutions=solutions, problem=problem)
        
        code_result = await self.programmer(problem=problem, analysis=ensemble_result['response'])
        
        final_solution = f"Ensemble solution: {ensemble_result['response']}\nCode verification: {code_result['output']}"
        return final_solution, self.llm.cost_manager.total_cost
                    