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
        self.sc_ensemble = operator.ScEnsemble(self.llm)
        self.programmer = operator.Programmer(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        analysis = await self.custom(input=problem, instruction=prompt_custom.ANALYZE_PROMPT)
        
        solutions = []
        for _ in range(3):  # Generate 3 solutions
            solution = await self.custom(input=problem + f"\nAnalysis: {analysis['response']}", instruction=prompt_custom.SOLVE_PROMPT)
            
            # Use Programmer to perform calculations if needed
            if "CALCULATE:" in solution['response']:
                calc_parts = solution['response'].split("CALCULATE:")
                for i in range(1, len(calc_parts)):
                    calc_result = await self.programmer(problem=calc_parts[i].strip())
                    calc_parts[i] = f"CALCULATE: {calc_parts[i].strip()}\nResult: {calc_result['output']}"
                solution['response'] = "".join(calc_parts)
            
            solutions.append(solution['response'])
        
        final_solution = await self.sc_ensemble(solutions=solutions, problem=problem)
        return final_solution['response'], self.llm.cost_manager.total_cost
                    