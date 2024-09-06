from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_53.prompt as prompt_custom
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
        solution = await self.custom(input=problem, instruction=prompt_custom.SOLVE_PROMPT)
        
        # Add a confidence check
        confidence = float(solution['response'].split('Confidence: ')[1].split('\n')[0])
        
        if confidence < 0.8:  # If confidence is below threshold, perform review and revision
            review_result = await self.review(problem=problem, solution=solution['response'])
            if not review_result['review_result']:
                solution = await self.revise(problem=problem, solution=solution['response'], feedback=review_result['feedback'])
        
        format_solution = await self.format(problem=problem, solution=solution['response'] if isinstance(solution, dict) else solution)
        return format_solution, self.llm.cost_manager.total_cost
                    