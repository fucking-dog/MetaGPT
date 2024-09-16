from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_18.prompt as prompt_custom
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
        self.generate = operator.Generate(self.llm)
        self.review = operator.Review(self.llm)
        self.revise = operator.Revise(self.llm)
        self.format = operator.Format(self.llm)
        self.sc_ensemble = operator.ScEnsemble(self.llm)
        self.custom = operator.Custom(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        # solutions = []
        # for _ in range(3):  # Generate multiple solutions for self-consistency
        #     solution = await self.generate(problem=problem)
        #     review_result = await self.review(problem=problem, solution=solution['response'])
        #
        #     if not review_result['review_result']:
        #         revised_solution = await self.revise(problem=problem, solution=solution['response'], feedback=review_result['feedback'])
        #         solution = revised_solution
        #
        #     solutions.append(solution['response'])
        #
        # # Apply self-consistency
        # sc_solution = await self.sc_ensemble(solutions=solutions, problem=problem)
        
        # Generate multiple solutions with different approaches
        multi_approach_solutions = []
        for approach in ["algebraic", "geometric", "numerical"]:
            approach_solution = await self.custom(input=f"Problem: {problem}\nApproach: {approach}", instruction=prompt_custom.MULTI_APPROACH_PROMPT)
            multi_approach_solutions.append(approach_solution['response'])
        
        # Select the best solution using ScEnsemble
        best_solution = await self.sc_ensemble(solutions=multi_approach_solutions, problem=problem)
        
        # Apply custom step for final refinement
        refined_solution = await self.custom(input=f"Problem: {problem}\nSolution: {best_solution['response']}", instruction=prompt_custom.REFINE_PROMPT)
        
        format_solution = await self.format(problem=problem, solution=refined_solution['response'])
        return format_solution['response'], self.llm.cost_manager.total_cost
                    