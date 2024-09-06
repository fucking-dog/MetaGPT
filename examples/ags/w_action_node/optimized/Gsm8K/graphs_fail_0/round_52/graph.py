from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_52.prompt as prompt_custom
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
        
        # Determine the mathematical domain(s)
        domains = await self.custom(input=rephrased_problem['rephrased_problem'], instruction=prompt_custom.DETERMINE_MATH_DOMAINS)
        
        # Generate solutions based on the determined domain(s)
        solutions = []
        for domain in domains['response'].split(','):
            if domain.strip() == 'algebra':
                solution = await self.custom(input=rephrased_problem['rephrased_problem'], instruction=prompt_custom.MATH_SOLUTION_PROMPT_ALGEBRAIC)
            elif domain.strip() == 'geometry':
                solution = await self.custom(input=rephrased_problem['rephrased_problem'], instruction=prompt_custom.MATH_SOLUTION_PROMPT_GEOMETRIC)
            else:
                solution = await self.custom(input=rephrased_problem['rephrased_problem'], instruction=prompt_custom.MATH_SOLUTION_PROMPT_ANALYTICAL)
            solutions.append(solution['response'])
        
        if len(solutions) > 1:
            combined_solution = await self.fu_ensemble(solutions=solutions, problem=problem)
            solution = combined_solution
        else:
            solution = {'response': solutions[0]}
        
        review_result = await self.review(problem=problem, solution=solution['response'])
        
        if not review_result['review_result']:
            revised_solution = await self.revise(problem=problem, solution=solution['response'], feedback=review_result['feedback'])
            solution['response'] = revised_solution['solution']
        
        format_solution = await self.format(problem=problem, solution=solution['response'])
        return format_solution, self.llm.cost_manager.total_cost
                    