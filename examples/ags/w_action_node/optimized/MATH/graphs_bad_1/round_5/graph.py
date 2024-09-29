from typing import Literal
import examples.ags.w_action_node.optimized.MATH.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.MATH.graphs.round_5.prompt as prompt_custom
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
        self.sc_ensemble = operator.ScEnsemble(self.llm)
        self.programmer = operator.Programmer(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        solutions = []
        
        # Generate solution using step-by-step approach
        step_solution = await self.custom(input=problem, instruction=prompt_custom.STEP_SOLVE_PROMPT)
        solutions.append(step_solution['response'])
        
        # Generate solution using mathematical concepts
        concept_solution = await self.custom(input=problem, instruction=prompt_custom.CONCEPT_SOLVE_PROMPT)
        solutions.append(concept_solution['response'])
        
        # Generate solution using programming approach
        code_solution = await self.programmer(problem=problem)
        solutions.append(code_solution['output'])
        
        # Use ScEnsemble to select the best solution
        final_solution = await self.sc_ensemble(solutions=solutions, problem=problem)
        
        return final_solution['response'], self.llm.cost_manager.total_cost
                    