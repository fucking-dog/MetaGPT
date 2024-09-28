from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_8.prompt as prompt_custom
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
        # Generate multiple initial solutions
        solutions = []
        for _ in range(3):
            initial_solution = await self.custom(input=problem, instruction=prompt_custom.SOLVE_PROMPT)
            solutions.append(initial_solution['response'])
        
        # Use ScEnsemble to select the best solution
        best_solution = await self.sc_ensemble(solutions=solutions, problem=problem)
        
        # Review and revise the best solution using Programmer
        review_instruction = f"Review and improve the following solution, ensuring all calculations are correct:\n{best_solution['response']}\nProblem: {problem}"
        reviewed_solution = await self.programmer(problem=review_instruction)
        
        # Final verification step
        verification_prompt = f"Verify the following solution:\n{reviewed_solution['output']}\nProblem: {problem}\nProvide the final answer as a number only."
        final_verification = await self.custom(input=verification_prompt, instruction=prompt_custom.VERIFY_PROMPT)
        
        return final_verification['response'], self.llm.cost_manager.total_cost
                    