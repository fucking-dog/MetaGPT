from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_58.prompt as prompt_custom
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
        self.format = operator.Format(self.llm)
        self.custom = operator.Custom(self.llm)
        self.rephrase = operator.Rephrase(self.llm)
        self.review = operator.Review(self.llm)
        self.fu_ensemble = operator.FuEnsemble(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        rephrased_problem = await self.rephrase(problem=problem)
        
        # Generate multiple solution approaches
        solution_approaches = []
        for strategy in ["ALGEBRAIC", "GEOMETRIC", "NUMERICAL"]:
            solution = await self.custom(input=rephrased_problem['rephrased_problem'], instruction=prompt_custom.MATH_PROBLEM_SOLVING.format(strategy=strategy))
            solution_approaches.append(solution['response'])
        
        # Use FuEnsemble to evaluate and synthesize
        enhanced_solution = await self.fu_ensemble(solutions=solution_approaches, problem=problem)
        
        review_result = await self.review(problem=problem, solution=enhanced_solution['solution'])
        
        if review_result['review_result']:
            format_solution = await self.format(problem=problem, solution=enhanced_solution['solution'])
            return format_solution, self.llm.cost_manager.total_cost
        else:
            revised_solution = await self.custom(input=f"{problem}\n\nPrevious solution: {enhanced_solution['solution']}\n\nFeedback: {review_result['feedback']}", instruction=prompt_custom.MATH_PROBLEM_REVISION)
            format_solution = await self.format(problem=problem, solution=revised_solution['response'])
            return format_solution, self.llm.cost_manager.total_cost
                    