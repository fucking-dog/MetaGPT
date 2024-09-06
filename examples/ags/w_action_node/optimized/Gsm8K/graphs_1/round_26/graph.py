from typing import Literal
from examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator import *
from examples.ags.w_action_node.optimized.Gsm8K.graphs.round_26.prompt import *
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
        self.sc_ensemble = ScEnsemble(self.llm)
        self.rephrase = Rephrase(self.llm)
        self.revise = Revise(self.llm)

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        think = await self.custom(input=problem, instruction=THINK_PROMPT)
        self_ask = await self.custom(input=problem + think['response'], instruction=SELF_ASK_PROMPT)
        rephrase = await self.rephrase(problem=problem)
        solutions = []
        for _ in range(3):  # Generate 3 solutions
            solution = await self.generate(problem=problem+think['response']+self_ask['response']+rephrase['rephrased_problem'])
            self_evaluate = await self.custom(input=problem + solution['response'], instruction=SELF_EVALUATE_PROMPT)
            solutions.append(solution['response'] + self_evaluate['response'])
        
        best_solution = await self.sc_ensemble(solutions=solutions, problem=problem)
        review_result = await self.review(problem=problem, solution=best_solution['solution'])
        if not review_result['review_result']:
            self_reflect = await self.custom(input=problem + best_solution['solution'] + review_result['feedback'], instruction=SELF_REFLECT_PROMPT)
            revised_solution = await self.revise(problem=problem, solution=best_solution['solution'], feedback=review_result['feedback'] + self_reflect['response'])
            solution = await self.generate(problem=problem+think['response']+self_ask['response']+rephrase['rephrased_problem']+revised_solution['solution'])
        else:
            solution = {'response': best_solution['solution']}
        format_solution = await self.format(problem=problem, solution=solution['response'])
        return format_solution, self.llm.cost_manager.total_cost
                    