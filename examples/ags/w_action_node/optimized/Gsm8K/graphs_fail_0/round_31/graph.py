from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_31.prompt as prompt_custom
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

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        solution = await self.custom(input=problem, instruction=prompt_custom.MATH_SOLUTION_PROMPT)
        format_solution = await self.format(problem=problem, solution=solution['response'])
        
        # Add a confidence check
        confidence_check = await self.custom(input=format_solution['solution'], instruction=prompt_custom.CONFIDENCE_CHECK_PROMPT)
        confidence = float(confidence_check['response'])
        
        if confidence < 0.8:  # If confidence is low, perform review and revision
            review_result = await self.review(problem=problem, solution=format_solution['solution'])
            if not review_result['review_result']:
                revised_solution = await self.revise(problem=problem, solution=format_solution['solution'], feedback=review_result['feedback'])
                format_solution = await self.format(problem=problem, solution=revised_solution['solution'])
        
        return format_solution, self.llm.cost_manager.total_cost
                    