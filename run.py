import asyncio

from metagpt.ext.aflow.benchmark.humaneval import HumanEvalBenchmark
from metagpt.ext.eflow.src.abstract import Workflow
from metagpt.ext.eflow.src.operators import CodeGenerate, Custom, ScEnsemble

llm_name_list = ["claude-3-5-sonnet-20240620", "gpt-4o-mini", "gpt-4o", "deepseek-chat"]


class MutliLLMWorkflow(Workflow):
    def __init__(self, name: str, llm_names: list, dataset: str):
        super().__init__(name, llm_names, dataset)
        self.custom = Custom(self.llm_dict["gpt-4o-mini"])
        self.code_generate = CodeGenerate(self.llm_dict["gpt-4o-mini"])
        self.sc_ensemble = ScEnsemble(self.llm_dict["claude-3-5-sonnet-20240620"])

    async def __call__(self, problem, function_name):
        solutions = []
        tasks = [
            self.code_generate(problem, function_name, self.llm_dict["claude-3-5-sonnet-20240620"]),
            self.code_generate(problem, function_name, self.llm_dict["gpt-4o-mini"]),
            self.code_generate(problem, function_name, self.llm_dict["gpt-4o"]),
            self.code_generate(problem, function_name, self.llm_dict["deepseek-chat"]),
        ]
        claude_solution, four_o_mini_solution, four_o_solution, deepseek_solution = await asyncio.gather(*tasks)

        solutions.append(claude_solution["solution"])
        solutions.append(four_o_mini_solution["solution"])
        solutions.append(four_o_solution["solution"])
        solutions.append(deepseek_solution["solution"])

        solution = await self.sc_ensemble(solutions, problem)

        return solution["response"], self.get_cost()


if __name__ == "__main__":

    async def main():
        graph = MutliLLMWorkflow(name="SelfConsistency", llm_names=llm_name_list, dataset="HumanEval")
        benchmark = HumanEvalBenchmark(
            name="HumanEval", file_path="metagpt/ext/aflow/data/humaneval_test.jsonl", log_path=""
        )
        avg_score = await benchmark.baseline_evaluation(graph, max_concurrent_tasks=5)
        return avg_score
    
    async def single_task():
        graph = MutliLLMWorkflow(name="SelfConsistency", llm_names=llm_name_list, dataset="HumanEval")
        task = "\n\ndef sum_to_n(n: int):\n    \"\"\"sum_to_n is a function that sums numbers from 1 to n.\n    >>> sum_to_n(30)\n    465\n    >>> sum_to_n(100)\n    5050\n    >>> sum_to_n(5)\n    15\n    >>> sum_to_n(10)\n    55\n    >>> sum_to_n(1)\n    1\n    \"\"\"\n"
        function_name = "sum_to_n" 
        solution, cost = await graph(task, function_name)
        print(solution)
        print(cost)

    asyncio.run(main())
