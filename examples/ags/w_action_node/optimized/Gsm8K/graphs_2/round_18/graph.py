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
        self.custom = Custom(self.llm)
        self.review = Review(self.llm)
        self.rephrase = Rephrase(self.llm)
        self.sc_ensemble = ScEnsemble(self.llm)
        self.fu_ensemble = FuEnsemble(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        rephrased_problem = await self.rephrase(problem=problem)
        think = await self.custom(input=problem + "\n\nRephrased problem: " + rephrased_problem['rephrased_problem'], instruction=THINK_PROMPT)
        
        # Generate multiple solutions
        solutions = []
        for _ in range(3):  # Generate three solutions
            solution = await self.generate(problem=problem+think['response'])
            solutions.append(solution['response'])
        
        # Use FuEnsemble to synthesize an enhanced integrated solution
        enhanced_solution = await self.fu_ensemble(solutions=solutions, problem=problem)
        
        review_result = await self.review(problem=problem, solution=enhanced_solution['solution'])
        if review_result['review_result']:
            format_solution = await self.format(problem=problem, solution=enhanced_solution['solution'])
        else:
            revised_solution = await self.generate(problem=problem+think['response']+review_result['feedback'])
            format_solution = await self.format(problem=problem, solution=revised_solution['response'])
        return format_solution, self.llm.cost_manager.total_cost
                    