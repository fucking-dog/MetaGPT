from typing import Literal
import examples.ags.w_action_node.optimized.MATH.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.MATH.graphs.round_6.prompt as prompt_custom
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
        # Step 1: Break down the problem
        breakdown = await self.custom(input=problem, instruction=prompt_custom.BREAKDOWN_PROMPT)
        
        # Step 2: Generate solutions for each part
        solutions = []
        for part in breakdown['response'].split('\n'):
            if part.strip():
                solution = await self.custom(input=part, instruction=prompt_custom.SOLVE_PROMPT)
                solutions.append(solution['response'])
        
        # Step 3: Perform calculations if needed
        for i, solution in enumerate(solutions):
            if "CALCULATE:" in solution:
                calc_problem = solution.split("CALCULATE:")[1].strip()
                calc_result = await self.programmer(problem=calc_problem)
                solutions[i] = solution.replace(f"CALCULATE: {calc_problem}", calc_result['output'])
        
        # Step 4: Combine solutions
        combined_solution = "\n".join(solutions)
        
        # Step 5: Generate final answer
        final_solution = await self.custom(input=problem + "\n" + combined_solution, instruction=prompt_custom.FINAL_ANSWER_PROMPT)
        
        return final_solution['response'], self.llm.cost_manager.total_cost
                    