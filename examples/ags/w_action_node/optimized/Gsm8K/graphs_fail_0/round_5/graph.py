from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_5.prompt as prompt_custom
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
        self.review = operator.Review(self.llm)
        self.revise = operator.Revise(self.llm)
        self.rephrase = operator.Rephrase(self.llm)
        self.fu_ensemble = operator.FuEnsemble(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        rephrased_problem = await self.rephrase(problem=problem)
        
        # Generate multiple solutions using different approaches
        solution1 = await self.custom(input=rephrased_problem['rephrased_problem'], instruction=prompt_custom.MATH_SOLUTION_PROMPT_ALGEBRAIC)
        solution2 = await self.custom(input=rephrased_problem['rephrased_problem'], instruction=prompt_custom.MATH_SOLUTION_PROMPT_GEOMETRIC)
        solution3 = await self.custom(input=rephrased_problem['rephrased_problem'], instruction=prompt_custom.MATH_SOLUTION_PROMPT_ANALYTICAL)
        
        # Ensemble the solutions
        enhanced_solution = await self.fu_ensemble(solutions=[solution1['response'], solution2['response'], solution3['response']], problem=rephrased_problem['rephrased_problem'])
        
        review_result = await self.review(problem=problem, solution=enhanced_solution['solution'])
        
        if review_result['review_result']:
            solution = enhanced_solution['solution']
        else:
            revised_solution = await self.revise(problem=problem, solution=enhanced_solution['solution'], feedback=review_result['feedback'])
            solution = revised_solution['solution']
        
        format_solution = await self.format(problem=problem, solution=solution)
        return format_solution, self.llm.cost_manager.total_cost
                    