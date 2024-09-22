from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_7.prompt as prompt_custom
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
        # Generate step-by-step solution
        step_solution = await self.custom(input=problem, instruction=prompt_custom.STEP_SOLVE_PROMPT)
        
        # Verify calculations using Programmer
        verify_instruction = f"Verify the calculations in this step-by-step solution:\n{step_solution['response']}\nProblem: {problem}"
        verified_solution = await self.programmer(problem=verify_instruction)
        
        # Generate final answer based on verified solution
        final_answer = await self.custom(input=f"Problem: {problem}\nVerified solution: {verified_solution['output']}", instruction=prompt_custom.FINAL_ANSWER_PROMPT)
        
        return final_answer['response'], self.llm.cost_manager.total_cost
                    