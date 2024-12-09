import asyncio
from metagpt.ext.aflow.benchmark.humaneval import HumanEvalBenchmark
from metagpt.ext.eflow.src.abstract import Workflow
from metagpt.ext.eflow.src.operators import CodeGenerate, Custom, ScEnsemble, MOAGenerate

llm_name_list = ["claude-3-5-sonnet-20240620", "gpt-4o-mini", "gpt-4o", "deepseek-chat"]

class MutliLLMWorkflow(Workflow):  
    def __init__(self, name: str, llm_names: list, dataset: str):
        super().__init__(name, llm_names, dataset)
        self.custom = Custom(self.llm_dict["gpt-4o-mini"])
        self.code_generate = CodeGenerate(self.llm_dict["gpt-4o-mini"])
        self.sc_ensemble = ScEnsemble(self.llm_dict["gpt-4o"])
        self.moa_generate = MOAGenerate(self.llm_dict["gpt-4o"])

    async def __call__(self, problem, function_name):
        solutions = []
        for i in range(3):
            solution = await self.moa_generate(problem, function_name, models=self.llm_dict.values())
            solutions.append(solution["solution"])

        solution = await self.sc_ensemble(solutions, problem)
        return solution["response"], self.get_cost()


class MoaWorkflow(Workflow):
    def __init__(self, name: str, llm_names: list, dataset: str):
        super().__init__(name, llm_names, dataset)
        self.moa_generate = MOAGenerate(self.llm_dict["gpt-4o"])
    
    async def __call__(self, problem, function_name):
        solution = await self.moa_generate(problem, function_name, models=self.llm_dict.values())
        return solution["solution"], self.get_cost()


if __name__ == "__main__":

    async def main():
        graph = MutliLLMWorkflow(name="SelfConsistency", llm_names=llm_name_list, dataset="HumanEval")
        benchmark = HumanEvalBenchmark(
            name="HumanEval", file_path="metagpt/ext/aflow/data/humaneval_incremental.jsonl", log_path=""
        )
        avg_score, avg_cost, total_cost = await benchmark.baseline_evaluation(graph, max_concurrent_tasks=5)
        return avg_score, avg_cost, total_cost
    
    async def single_task():
        graph = MoaWorkflow(name="Moa", llm_names=llm_name_list, dataset="HumanEval")
        # graph = MutliLLMWorkflow(name="SelfConsistency", llm_names=llm_name_list, dataset="HumanEval")
        task = "\n\ndef sum_to_n(n: int):\n    \"\"\"sum_to_n is a function that sums numbers from 1 to n.\n    >>> sum_to_n(30)\n    465\n    >>> sum_to_n(100)\n    5050\n    >>> sum_to_n(5)\n    15\n    >>> sum_to_n(10)\n    55\n    >>> sum_to_n(1)\n    1\n    \"\"\"\n"
        function_name = "sum_to_n" 
        solution, cost = await graph(task, function_name)
        print(solution)
        print(cost)

    async def moa_workflow():
        graph = MoaWorkflow(name="Moa", llm_names=llm_name_list, dataset="HumanEval")
        benchmark = HumanEvalBenchmark(
            name="HumanEval", file_path="metagpt/ext/aflow/data/humaneval_incremental.jsonl", log_path=""
        )
        avg_score, avg_cost, total_cost = await benchmark.baseline_evaluation(graph, max_concurrent_tasks=5)
        return avg_score, avg_cost, total_cost

    sc_moa_score, sc_moa_cost, sc_moa_total_cost = asyncio.run(main())
    moa_score, moa_cost, moa_total_cost = asyncio.run(moa_workflow())
    print(f"SelfConsistency: {sc_moa_score}, {sc_moa_cost}, {sc_moa_total_cost}")
    print(f"Moa: {moa_score}, {moa_cost}, {moa_total_cost}")
