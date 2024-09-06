from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_49.prompt as prompt_custom
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
        domain = await self.custom(input=rephrased_problem['rephrased_problem'], instruction=prompt_custom.DETERMINE_MATH_DOMAIN)
        
        # Generate solutions based on the determined domain(s)
        if 'combination' in domain['response']:
            solution = await self.custom(input=rephrased_problem['rephrased_problem'], instruction=prompt_custom.MATH_SOLUTION_PROMPT_COMBINED)
        elif 'algebra' in domain['response']:
            solution = await self.custom(input=rephrased_problem['rephrased_problem'], instruction=prompt_custom.MATH_SOLUTION_PROMPT_ALGEBRAIC)
        elif 'geometry' in domain['response']:
            solution = await self.custom(input=rephrased_problem['rephrased_problem'], instruction=prompt_custom.MATH_SOLUTION_PROMPT_GEOMETRIC)
        else:
            solution = await self.custom(input=rephrased_problem['rephrased_problem'], instruction=prompt_custom.MATH_SOLUTION_PROMPT_ANALYTICAL)
        
        review_result = await self.review(problem=problem, solution=solution['response'])
        
        if not review_result['review_result']:
            revised_solution = await self.revise(problem=problem, solution=solution['response'], feedback=review_result['feedback'])
            solution['response'] = revised_solution['solution']
        
        format_solution = await self.format(problem=problem, solution=solution['response'])
        return format_solution, self.llm.cost_manager.total_cost
                    