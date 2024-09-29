from typing import Literal
import examples.ags.w_action_node.optimized.MATH.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.MATH.graphs.round_7.prompt as prompt_custom
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
        initial_analysis = await self.custom(input=problem, instruction=prompt_custom.DETAILED_ANALYSIS_PROMPT)
        
        try:
            code_generation = await self.programmer(problem=problem, analysis=initial_analysis['response'])
            if code_generation['output']:
                calculation_validation = await self.custom(input=f"{problem}\n\nPython calculation result: {code_generation['output']}", instruction=prompt_custom.CALCULATION_VALIDATION_PROMPT)
                validated_result = calculation_validation['response']
            else:
                validated_result = "No valid calculation result."
        except Exception:
            validated_result = "Error in code generation or execution."
        
        solutions = []
        for _ in range(3):  # Generate 3 solutions
            if validated_result != "No valid calculation result." and validated_result != "Error in code generation or execution.":
                solution = await self.custom(input=f"{problem}\n\nValidated calculation result: {validated_result}", instruction=prompt_custom.FINAL_SOLUTION_PROMPT)
            else:
                solution = await self.custom(input=problem, instruction=prompt_custom.FALLBACK_SOLUTION_PROMPT)
            solutions.append(solution['response'])
        
        final_solution = await self.sc_ensemble(solutions=solutions, problem=problem)
        
        consistency_check = await self.custom(input=f"{problem}\n\nProposed solution: {final_solution['response']}", instruction=prompt_custom.CONSISTENCY_CHECK_PROMPT)
        
        if "consistent" in consistency_check['response'].lower():
            return final_solution['response'], self.llm.cost_manager.total_cost
        else:
            refined_solution = await self.custom(input=f"{problem}\n\nInitial solution: {final_solution['response']}\nConsistency check: {consistency_check['response']}", instruction=prompt_custom.REFINE_SOLUTION_PROMPT)
            return refined_solution['response'], self.llm.cost_manager.total_cost
                    