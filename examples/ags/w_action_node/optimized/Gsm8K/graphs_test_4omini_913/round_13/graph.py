from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_13.prompt as prompt_custom
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
        self.review = operator.Review(self.llm)
        self.revise = operator.Revise(self.llm)
        self.custom = operator.Custom(self.llm)
        self.fu_ensemble = operator.FuEnsemble(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        # Generate multiple alternative approaches
        approaches = []
        for _ in range(3):
            approach = await self.custom(input=problem, instruction=prompt_custom.ALTERNATIVE_APPROACH)
            approaches.append(approach['response'])
        
        # Generate solutions using different approaches
        solutions = []
        for approach in approaches:
            solution = await self.generate(problem=f"question:{problem}, approach:{approach}")
            solutions.append(solution['response'])
        
        # Use FuEnsemble to evaluate and synthesize the solutions
        ensemble_solution = await self.fu_ensemble(solutions=solutions, problem=problem)
        
        review_result = await self.review(problem=problem, solution=ensemble_solution['response'])
        
        if not review_result['review_result']:
            context = await self.custom(input=problem + f" Original solution: {ensemble_solution['response']}", instruction=prompt_custom.REVISION_CONTEXT)
            revised_solution = await self.revise(problem=problem, solution=ensemble_solution['response'], feedback=review_result['feedback'] + f" Additional context: {context['response']}")
            solution = revised_solution
        else:
            solution = ensemble_solution
        
        format_solution = await self.format(problem=problem, solution=solution['response'])
        return format_solution['response'], self.llm.cost_manager.total_cost
                    