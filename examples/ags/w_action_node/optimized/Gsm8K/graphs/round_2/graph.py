from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_2.prompt as prompt_custom
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
        initial_solution = await self.custom(input=problem, instruction=prompt_custom.SOLVE_PROMPT)
        
        review_instruction = f"Review and verify the following solution:\n{initial_solution['response']}\nProblem: {problem}"
        reviewed_solution = await self.programmer(problem=review_instruction)
        
        final_solution = reviewed_solution['output'] if reviewed_solution['output'] else initial_solution['response']
        
        return final_solution, self.llm.cost_manager.total_cost
                    