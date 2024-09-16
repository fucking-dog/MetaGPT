from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_22.prompt as prompt_custom
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
        self.custom = operator.Custom(self.llm)
        self.rephrase = operator.Rephrase(self.llm)
        self.sc_ensemble = operator.ScEnsemble(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        rephrased_problem = await self.rephrase(problem=problem)
        
        # Generate multiple solutions using different approaches
        solutions = []
        for _ in range(3):
            solution = await self.generate(problem=f"Original problem: {problem}\nRephrased problem: {rephrased_problem['response']}")
            solutions.append(solution['response'])
        
        # Use ScEnsemble to select the best solution
        best_solution = await self.sc_ensemble(solutions=solutions, problem=problem)
        
        review_result = await self.review(problem=problem, solution=best_solution['response'])
        
        if not review_result['review_result']:
            best_solution = await self.revise(problem=problem, solution=best_solution['response'], feedback=review_result['feedback'])
        
        final_solution = await self.custom(input=f"Problem: {problem}\nSolution: {best_solution['response']}", instruction=prompt_custom.FINAL_SOLUTION_PROMPT)
        
        return final_solution['response'], self.llm.cost_manager.total_cost
                    