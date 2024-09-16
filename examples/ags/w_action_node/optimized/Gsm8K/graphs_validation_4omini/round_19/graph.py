from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_19.prompt as prompt_custom
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
        self.rephrase = operator.Rephrase(self.llm)
        self.review = operator.Review(self.llm)
        self.revise = operator.Revise(self.llm)
        self.custom = operator.Custom(self.llm)
        self.fu_ensemble = operator.FuEnsemble(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        rephrased_problem = await self.rephrase(problem=problem)
        
        # Analyze problem structure and identify key components
        problem_analysis = await self.custom(input=rephrased_problem['response'], instruction=prompt_custom.ANALYZE_PROBLEM)
        
        # Generate multiple solutions using different approaches
        solution1 = await self.generate(problem=f"Problem: {rephrased_problem['response']}\nAnalysis: {problem_analysis['response']}")
        solution2 = await self.custom(input=f"Problem: {rephrased_problem['response']}\nAnalysis: {problem_analysis['response']}", instruction=prompt_custom.ALTERNATIVE_APPROACH)
        solution3 = await self.custom(input=f"Problem: {rephrased_problem['response']}\nAnalysis: {problem_analysis['response']}", instruction=prompt_custom.CREATIVE_SOLUTION)
        
        # Use FuEnsemble to evaluate and synthesize the solutions
        solutions = [solution1['response'], solution2['response'], solution3['response']]
        enhanced_solution = await self.fu_ensemble(solutions=solutions, problem=problem)
        
        review_result = await self.review(problem=problem, solution=enhanced_solution['response'])
        if not review_result['review_result']:
            enhanced_solution = await self.revise(problem=problem, solution=enhanced_solution['response'], feedback=review_result['feedback'])
        
        final_solution = await self.custom(input=f"Problem: {problem}\nAnalysis: {problem_analysis['response']}\nSolution: {enhanced_solution['response']}", instruction=prompt_custom.ENHANCE_SOLUTION)
        format_solution = await self.format(problem=problem, solution=final_solution['response'])
        return format_solution['response'], self.llm.cost_manager.total_cost
                    