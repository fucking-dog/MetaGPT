from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_11.prompt as prompt_custom
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
        self.custom = operator.Custom(self.llm)
        self.programmer = operator.Programmer(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        analysis = await self.custom(input=problem, instruction=prompt_custom.ANALYZE_PROMPT)
        code_solution = await self.programmer(problem=problem, analysis=analysis['response'])
        final_solution = await self.custom(input=f"Problem: {problem}\nAnalysis: {analysis['response']}\nCode Solution: {code_solution['output']}", instruction=prompt_custom.FINAL_PROMPT)
        return final_solution['response'], self.llm.cost_manager.total_cost
                    