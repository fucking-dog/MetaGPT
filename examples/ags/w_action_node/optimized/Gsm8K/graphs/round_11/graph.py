from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_11.prompt as prompt_custom
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
        # Extract key information
        key_info = await self.custom(input=problem, instruction=prompt_custom.EXTRACT_KEY_INFO_PROMPT)
        
        solutions = []
        for _ in range(3):  # Generate 3 solutions
            initial_solution = await self.custom(input=problem + "\nKey Information: " + key_info['response'], instruction=prompt_custom.SOLVE_PROMPT)
            solutions.append(initial_solution['response'])
        
        ensemble_result = await self.sc_ensemble(solutions=solutions, problem=problem)
        
        # Review and refine the solution
        review_instruction = f"Review and refine the following solution:\n{ensemble_result['response']}\nProblem: {problem}\nKey Information: {key_info['response']}"
        reviewed_solution = await self.custom(input=review_instruction, instruction=prompt_custom.REVIEW_REFINE_PROMPT)
        
        # Final verification
        verification_instruction = f"Verify the following solution:\n{reviewed_solution['response']}\nProblem: {problem}\nKey Information: {key_info['response']}"
        verified_solution = await self.programmer(problem=verification_instruction)
        
        final_solution = verified_solution['output'] if verified_solution['output'] else reviewed_solution['response']
        
        return final_solution, self.llm.cost_manager.total_cost
                    