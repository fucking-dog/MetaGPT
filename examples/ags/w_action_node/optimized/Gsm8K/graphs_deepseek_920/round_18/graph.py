from typing import Literal
import examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.Gsm8K.graphs.round_18.prompt as prompt_custom
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
        solution = await self.custom(input=problem, instruction=prompt_custom.SOLVE_PROMPT)
        extracted_answer = await self.custom(input=solution['response'], instruction=prompt_custom.EXTRACT_ANSWER_PROMPT)
        verification = await self.programmer(
            problem=f"Problem: {problem}\nCalculated answer: {extracted_answer['response']}",
            analysis="Verify if the calculated answer is correct. If not, provide the correct answer with explanation."
        )
        final_answer = await self.custom(input=f"{problem}\n{solution['response']}\n{verification['output']}", instruction=prompt_custom.FINAL_ANSWER_PROMPT)
        return final_answer['response'], self.llm.cost_manager.total_cost
                    