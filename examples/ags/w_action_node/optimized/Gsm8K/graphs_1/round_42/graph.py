from typing import Literal
from examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator import *
from examples.ags.w_action_node.optimized.Gsm8K.graphs.round_42.prompt import *
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
            solutions.append(solution['response'])
        
        best_solution = await self.sc_ensemble(solutions=solutions, problem=problem)
        review_result = await self.review(problem=problem, solution=best_solution['solution'])
        revision_count = 0
        while not review_result['review_result'] and revision_count < 3:
            if revision_count > 0:
                self_reflection = await self.custom(input=problem + best_solution['solution'] + review_result['feedback'], instruction=SELF_REFLECT_PROMPT)
                solution = await self.generate(problem=problem+think['response']+self_ask['response']+rephrase['rephrased_problem']+review_result['feedback']+self_reflection['response'])
            else:
                solution = await self.generate(problem=problem+think['response']+self_ask['response']+rephrase['rephrased_problem']+review_result['feedback'])
            best_solution['solution'] = solution['response']
            review_result = await self.review(problem=problem, solution=best_solution['solution'])
            revision_count += 1
        
        format_solution = await self.format(problem=problem, solution=best_solution['solution'])
        return format_solution, self.llm.cost_manager.total_cost
                    