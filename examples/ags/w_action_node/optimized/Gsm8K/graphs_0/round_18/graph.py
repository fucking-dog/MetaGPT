from typing import Literal
from examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator import *
from examples.ags.w_action_node.optimized.Gsm8K.graphs.round_18.prompt import *
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
        self.verify = Verify(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        question = await self.generate(input=problem, prompt=REPHRASE_PROMPT)
        solution = await self.generate(input=question['content'], prompt=GENERATE_PROMPT)
        verified_solution = await self.verify(input=solution['content'], prompt=VERIFY_PROMPT)
        format_solution = await self.format(input=f"Original question:{problem} \n\nFinal solution:{verified_solution['content']}")
        return format_solution, self.llm.cost_manager.total_cost
                    