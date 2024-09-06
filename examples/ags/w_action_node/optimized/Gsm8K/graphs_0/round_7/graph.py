from typing import Literal
from examples.ags.w_action_node.optimized.Gsm8K.graphs.template.operator import *
from examples.ags.w_action_node.optimized.Gsm8K.graphs.round_7.prompt import *
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

    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        question = await self.generate(input=problem, prompt=REPHRASE_PROMPT)
        self_questions = await self.generate(input=question['content'], prompt=SELF_QUESTION_PROMPT)
        breakdown = await self.generate(input=f"Problem: {question['content']}", prompt=BREAKDOWN_PROMPT)
        solution = await self.generate(input=f"Problem: {question['content']}\n\nSelf-questions and answers: {self_questions['content']}\n\nProblem breakdown: {breakdown['content']}", prompt=GENERATE_PROMPT)
        error_check = await self.generate(input=f"Problem: {problem}\n\nSolution: {solution['content']}", prompt=ERROR_CHECK_PROMPT)
        if "errors are found" in error_check['content'].lower():
            solution = await self.generate(input=f"Problem: {problem}\n\nOriginal solution: {solution['content']}\n\nError check feedback: {error_check['content']}", prompt=GENERATE_PROMPT)
        review = await self.generate(input=f"Problem: {problem}\n\nSolution: {solution['content']}", prompt=REVIEW_PROMPT)
        if "issues are found" in review['content'].lower():
            solution = await self.generate(input=f"Problem: {problem}\n\nOriginal solution: {solution['content']}\n\nReview feedback: {review['content']}", prompt=GENERATE_PROMPT)
        format_solution = await self.format(input=f"Original question:{problem} \n\nFinal solution:{solution['content']}")
        return format_solution, self.llm.cost_manager.total_cost
                    