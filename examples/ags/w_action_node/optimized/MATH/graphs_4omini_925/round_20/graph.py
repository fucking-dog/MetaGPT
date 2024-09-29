from typing import Literal
import examples.ags.w_action_node.optimized.MATH.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.MATH.graphs.round_20.prompt as prompt_custom
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
        solutions = []
        approaches = ['algebraic', 'geometric', 'numerical', 'analytical']
        
        for approach in approaches:
            solution = await self.custom(input=problem, instruction=f"{prompt_custom.SOLVE_PROMPT} Use a {approach} approach if possible.")
            solutions.append(solution['response'])
        
        code_solution = await self.programmer(problem=problem, analysis="Generate Python code to solve this problem numerically if possible.")
        if code_solution['output']:
            solutions.append(code_solution['output'])
        
        ensemble_solution = await self.sc_ensemble(solutions=solutions, problem=problem)
        
        final_review = await self.custom(input=f"Problem: {problem}\nProposed solution: {ensemble_solution['response']}", instruction=prompt_custom.REVIEW_PROMPT)
        
        return final_review['response'], self.llm.cost_manager.total_cost
                    