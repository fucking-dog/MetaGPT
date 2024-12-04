from typing import List, Tuple

from pydantic import BaseModel, Field

from metagpt.configs.models_config import ModelsConfig
from metagpt.ext.aflow.benchmark.humaneval import HumanEvalBenchmark
from metagpt.ext.aflow.scripts.operator import Operator
from metagpt.ext.aflow.scripts.workflow import Workflow
from metagpt.llm import LLM

HUMANEVAL_PROMPT_IO = """
{question}\nGenerate an answer to this question, without any additional test cases. 
"""

WITHOUT_PROMPT = """
{question}
"""

SC_ENSEMBLE_PROMPT = """
Given the question described as follows: {question}
Several solutions have been generated to address the given question. They are as follows:
{solutions}

Carefully evaluate these solutions and identify the answer that appears most frequently across them. This consistency in answers is crucial for determining the most reliable solution.

In the "thought" field, provide a detailed explanation of your thought process. In the "solution_letter" field, output only the single letter ID (A, B, C, etc.) corresponding to the most consistent solution. Do not include any additional text or explanation in the "solution_letter" field.
"""


class GenerateOp(BaseModel):
    solution: str = Field(default="", description="Python Solution For This Question.")


class ScEnsembleOp(BaseModel):
    thought: str = Field(default="", description="The thought of the most consistent solution.")
    solution_letter: str = Field(default="", description="The letter of most consistent solution.")


class Generate(Operator):
    def __init__(self, llm: LLM, name: str = "Generate"):
        super().__init__(llm, name)

    async def __call__(self, question: str, entry_point: str) -> Tuple[str, str]:
        prompt = WITHOUT_PROMPT.format(question=question)
        response = await self._fill_node(GenerateOp, prompt, mode="code_fill", function_name=entry_point)
        return response


class JSONGenerate(Operator):
    def __init__(self, llm: LLM, name: str = "JSONGenerate"):
        super().__init__(llm, name)

    async def __call__(self, question: str, entry_point: str) -> Tuple[str, str]:
        prompt = WITHOUT_PROMPT.format(question=question)
        response = await self._fill_node(GenerateOp, mode="single_fill", prompt=prompt)
        return response


class ScEnsemble(Operator):
    def __init__(self, llm: LLM, name: str = "ScEnsemble"):
        super().__init__(llm, name)

    async def __call__(self, solutions: List[str], problem: str):
        answer_mapping = {}
        solution_text = ""
        for index, solution in enumerate(solutions):
            answer_mapping[chr(65 + index)] = index
            solution_text += f"{chr(65 + index)}: \n{str(solution)}\n\n\n"

        prompt = SC_ENSEMBLE_PROMPT.format(question=problem, solutions=solution_text)
        response = await self._fill_node(ScEnsembleOp, prompt, mode="xml_fill")

        answer = response.get("solution_letter", "")
        answer = answer.strip().upper()

        return {"response": solutions[answer_mapping[answer]]}


class IOSolveGraph(Workflow):
    def __init__(self, name: str, llm_config, dataset: str):
        super().__init__(name, llm_config, dataset)
        self.generate = Generate(self.llm)

    async def __call__(self, question, entry_point):
        solution = await self.generate(question, entry_point)
        return solution["solution"], self.llm.cost_manager.total_cost


class JSONSolveGraph(Workflow):
    def __init__(self, name: str, llm_config, dataset: str):
        super().__init__(name, llm_config, dataset)
        self.generate = Generate(self.llm)

    async def __call__(self, question, entry_point):
        solution = await self.generate(question, entry_point)
        return solution["solution"], self.llm.cost_manager.total_cost


class SelfConsistencyGraph(Workflow):
    def __init__(self, name: str, llm_config, dataset: str):
        super().__init__(name, llm_config, dataset)
        self.generate = Generate(llm=self.llm)
        self.sc_ensemble = ScEnsemble(llm=self.llm)

    async def __call__(self, problem, function_name):
        solutions = []
        for i in range(5):
            solution = await self.generate(problem, function_name)
            solutions.append(solution["solution"])
        solution = await self.sc_ensemble(solutions, problem)
        return solution["response"], self.llm.cost_manager.total_cost


if __name__ == "__main__":

    async def main():
        # llm_config = ModelsConfig.default().get("llama-3.2-90b-vision-instruct")
        llm_config = ModelsConfig.default().get("meta-llama/Meta-Llama-3.1-70B-Instruct")
        # llm_config = ModelsConfig.default().get("gpt-4o-mini")
        # llm_config = ModelsConfig.default().get("gpt-4o")
        # llm_config = ModelsConfig.default().get("deepseek-chat")
        # llm_config = ModelsConfig.default().get("claude-3-5-sonnet-20240620")
        # graph = IOSolveGraph(name="IO", llm_config=llm_config, dataset="HumanEval")
        # graph = JSONSolveGraph(name="JSON", llm_config=llm_config, dataset="HumanEval")
        graph = SelfConsistencyGraph(name="SelfConsistency", llm_config=llm_config, dataset="HumanEval")
        benchmark = HumanEvalBenchmark(
            name="HumanEval",
            file_path="/Users/trl/Github_project/MetaGPT-MathAI/metagpt/ext/aflow/data/humaneval_test.jsonl",
            log_path="",
        )
        avg_score = await benchmark.baseline_evaluation(graph, max_concurrent_tasks=5)
        return avg_score

    import asyncio

    asyncio.run(main())


# llama + markdown + prompt 0.75573

# gpt-4o-mini + markdown + prompt  0.871
# gpt-4o-mini + json + prompt  0.81679
# gpt-4o-mini
