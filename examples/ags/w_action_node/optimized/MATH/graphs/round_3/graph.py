from typing import Literal
import examples.ags.w_action_node.optimized.MATH.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.MATH.graphs.round_3.prompt as prompt_custom
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
        self.sc_ensemble = operator.ScEnsemble(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        # Use Programmer to generate and execute Python code
        code_solution = await self.programmer(problem=problem)
        
        # Use Custom to refine and format the answer
        refined_solution = await self.custom(input=problem + f"\nCode output: {code_solution['output']}", instruction=prompt_custom.REFINE_ANSWER_PROMPT)
        
        # Generate multiple solutions using Custom
        solutions = []
        for _ in range(3):
            solution = await self.custom(input=problem, instruction=prompt_custom.GENERATE_SOLUTION_PROMPT)
            solutions.append(solution['response'])
        
        # Use ScEnsemble to select the most consistent solution
        final_solution = await self.sc_ensemble(solutions=solutions, problem=problem)
        
        return final_solution['response'], self.llm.cost_manager.total_cost
                    