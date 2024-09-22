from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_13.prompt as prompt_custom
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
        solution1 = await self.custom(input=problem, instruction=prompt_custom.SOLVE_PROMPT)
        solution2 = await self.custom(input=problem, instruction=prompt_custom.ALTERNATIVE_SOLVE_PROMPT)
        
        verify_initial = await self.custom(input=f"Problem: {problem}\nSolution 1: {solution1['response']}\nSolution 2: {solution2['response']}", instruction=prompt_custom.VERIFY_INITIAL_SOLUTIONS_PROMPT)
        
        breakdown = await self.custom(input=f"Problem: {problem}\nSolution 1: {solution1['response']}\nSolution 2: {solution2['response']}\nVerification: {verify_initial['response']}", instruction=prompt_custom.BREAKDOWN_PROMPT)
        
        validation = await self.programmer(problem=problem, analysis=breakdown['response'])
        
        ensemble = await self.custom(input=f"Problem: {problem}\nSolution 1: {solution1['response']}\nSolution 2: {solution2['response']}\nBreakdown: {breakdown['response']}\nValidation: {validation['output']}", instruction=prompt_custom.ENSEMBLE_PROMPT)
        
        verification = await self.custom(input=f"Problem: {problem}\nEnsemble Solution: {ensemble['response']}\nValidation: {validation['output']}", instruction=prompt_custom.VERIFY_PROMPT)
        
        final_solution = verification['response']
        
        extracted_answer = await self.custom(input=final_solution, instruction=prompt_custom.EXTRACT_ANSWER_PROMPT)
        
        try:
            numerical_answer = float(extracted_answer['response'])
        except ValueError:
            numerical_answer = None
        
        return numerical_answer, self.llm.cost_manager.total_cost
                    