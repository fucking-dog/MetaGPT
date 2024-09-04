from typing import Literal
from examples.ags.w_action_node.optimized.Gsm8K.operators.ContextualGenerate.round_2.operator import *
from examples.ags.w_action_node.optimized.Gsm8K.operators.ContextualGenerate.round_2.prompt import *
from examples.ags.w_action_node.optimized.Gsm8K.operators.template.operator import Format, Generate
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
        self.contextual_generate = ContextualGenerate(self.llm)

    async def __call__(self, problem: str):
        context = "Let's approach this step-by-step:"
        solution = await self.contextual_generate(problem, context)
        print(solution)
        format_solution = await self.format(problem=problem, solution=solution['response'])
        return format_solution, self.llm.cost_manager.total_cost

                    