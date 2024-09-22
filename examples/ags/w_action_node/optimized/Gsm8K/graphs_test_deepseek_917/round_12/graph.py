from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_12.prompt as prompt_custom
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
        self.format = operator.Format(self.llm)
        self.custom = operator.Custom(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        problem_analysis = await self.custom(input=problem, instruction=prompt_custom.ANALYZE_PROMPT)
        
        solution1 = await self.custom(input=problem, instruction=prompt_custom.SOLVE_PROMPT1)
        solution2 = await self.custom(input=problem, instruction=prompt_custom.SOLVE_PROMPT2)
        solution3 = await self.custom(input=problem, instruction=prompt_custom.SOLVE_PROMPT3)
        
        integrated_solution = await self.custom(
            input=f"Problem: {problem}\nAnalysis: {problem_analysis['response']}\nSolution 1: {solution1['response']}\nSolution 2: {solution2['response']}\nSolution 3: {solution3['response']}",
            instruction=prompt_custom.INTEGRATE_PROMPT
        )
        
        reviewed_solution = await self.custom(
            input=f"Problem: {problem}\nIntegrated Solution: {integrated_solution['response']}",
            instruction=prompt_custom.REVIEW_PROMPT
        )
        
        numerical_check = await self.custom(
            input=f"Problem: {problem}\nProblem Analysis: {problem_analysis['response']}\nReviewed Solution: {reviewed_solution['response']}",
            instruction=prompt_custom.NUMERICAL_CHECK_PROMPT
        )
        
        self_reflection = await self.custom(
            input=f"Problem: {problem}\nSolution after numerical check: {numerical_check['response']}",
            instruction=prompt_custom.SELF_REFLECTION_PROMPT
        )
        
        format_solution = await self.format(problem=problem, solution=self_reflection['response'])
        return format_solution['response'], self.llm.cost_manager.total_cost
                    