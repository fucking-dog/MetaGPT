from typing import Literal
from examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator import *
from examples.ags.w_action_node.optimized.Gsm8K.graphs.round_54.prompt import *
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
        self.generate = Generate(self.llm)
        self.format = Format(self.llm)
        self.custom = Custom(self.llm)
        self.review = Review(self.llm)
        self.revise = Revise(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        think = await self.custom(input=problem, instruction=THINK_PROMPT)
        solution = await self.generate(problem=problem+think['response'])
        review_result = await self.review(problem=problem, solution=solution['response'])
        if not review_result['review_result']:
            solution = await self.revise(problem=problem, solution=solution['response'], feedback=review_result['feedback'])
        format_solution = await self.format(problem=problem, solution=solution['response'])
        return format_solution, self.llm.cost_manager.total_cost
                    