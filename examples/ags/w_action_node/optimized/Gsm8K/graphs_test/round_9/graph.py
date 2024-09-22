from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_9.prompt as prompt_custom
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

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        step_by_step_solution = await self.custom(input=problem, instruction=prompt_custom.SOLVE_PROMPT)
        
        review_instruction = f"Review and verify the following step-by-step solution:\n{step_by_step_solution['response']}\nProblem: {problem}\nIf there are any errors, provide the corrected solution. If the solution is correct, simply state 'The solution is correct.'"
        reviewed_solution = await self.programmer(problem=review_instruction)
        
        if "The solution is correct" in reviewed_solution['output']:
            final_solution = step_by_step_solution['response']
        else:
            final_solution = reviewed_solution['output']
        
        return final_solution, self.llm.cost_manager.total_cost
                    