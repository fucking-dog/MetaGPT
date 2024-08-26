from typing import Literal
from examples.ags.w_action_node.optimized.Gsm8K.graphs.round_2.operator import *
from examples.ags.w_action_node.optimized.Gsm8K.graphs.round_2.prompt import *
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

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        breakdown = await self.generate(problem, prompt="Break down this problem into smaller, manageable parts: {problem}")
        solution_parts = []
        for part in breakdown.split('\n'):
            part_solution = await self.generate(part, prompt=GENERATE_PROMPT)
            solution_parts.append(part_solution)
        
        final_solution = await self.generate("\n".join(solution_parts), prompt="Combine these partial solutions into a complete, coherent solution for the original problem:")
        return final_solution, self.llm.cost_manager.total_cost
                    