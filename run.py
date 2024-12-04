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

        solutions.append(claude_solution)
        solutions.append(four_o_mini_solution)
        solutions.append(four_o_solution)
        solutions.append(deepseek_solution)

        solution = await self.sc_ensemble(solutions, problem)

        return solution["response"], self.get_cost()


if __name__ == "__main__":

    async def main():
        # llm_config = ModelsConfig.default().get("llama-3.2-90b-vision-instruct")

        graph = MutliLLMWorkflow(name="SelfConsistency", llm_names=llm_name_list, dataset="HumanEval")
        benchmark = HumanEvalBenchmark(
            name="HumanEval",
            file_path="/Users/trl/Github_project/MetaGPT-MathAI/metagpt/ext/aflow/data/humaneval_test.jsonl",
            log_path="",
        )
        avg_score = await benchmark.baseline_evaluation(graph, max_concurrent_tasks=5)
        return avg_score

    import asyncio

    asyncio.run(main())
