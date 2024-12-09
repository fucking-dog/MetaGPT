from metagpt.ext.eflow.src.abstract import Workflow
from metagpt.ext.eflow.src.operators import Custom, Test, MOAGenerate, MOATest

llm_name_list = ["claude-3-5-sonnet-20240620", "gpt-4o-mini", "gpt-4o", "deepseek-chat"]

IMPROVE_CODE_PROMPT = """
The previous solution failed some test cases. Please analyze the problem carefully and provide an improved solution that addresses all edge cases and requirements. Ensure your code is efficient and follows best practices.
"""

class MoaAflowWorkflow(Workflow):
    def __init__(
        self,
        name: str,
        llm_names: list,
        dataset: str,
    ) -> None:
        super().__init__(name, llm_names, dataset)
        self.custom = Custom(self.llm_dict["gpt-4o-mini"])
        self.test = Test(self.llm_dict["gpt-4o"])
        self.moa_generate = MOAGenerate(self.llm_dict["gpt-4o"])

    async def __call__(self, problem: str, entry_point: str):
        """
        Implementation of the MOA workflow
        """
        solution = await self.moa_generate(problem, entry_point, models=self.llm_dict.values())
        test_result = await self.test(problem=problem, solution=solution['solution'], entry_point=entry_point)
        
        if test_result['result']:
            return test_result['solution'], self.get_cost()
        else:
            # If the test fails, try to generate a new solution with MOA
            problem = problem + "\n" + IMPROVE_CODE_PROMPT
            new_solution = await self.moa_generate(problem, entry_point, models=self.llm_dict.values())
            return new_solution['solution'], self.get_cost()
        

class MoaAflowTestWorkflow(Workflow):
    def __init__(
        self,
        name: str,
        llm_names: list,
        dataset: str,
    ) -> None:
        super().__init__(name, llm_names, dataset)
        self.custom = Custom(self.llm_dict["gpt-4o-mini"])
        self.test = Test(self.llm_dict["gpt-4o"])
        self.moa_generate = MOAGenerate(self.llm_dict["gpt-4o"])
        self.moa_test = MOATest(self.llm_dict["gpt-4o"])

    async def __call__(self, problem: str, entry_point: str):
        """
        Implementation of the MOA workflow
        """
        solution = await self.moa_generate(problem, entry_point, models=self.llm_dict.values())
        test_result = await self.moa_test(problem=problem, solution=solution['solution'], entry_point=entry_point, models=self.llm_dict.values())
        
        if test_result['result']:
            return test_result['solution'], self.get_cost()
        else:
            # If the test fails, try to generate a new solution with MOA
            problem = problem + "\n" + IMPROVE_CODE_PROMPT
            new_solution = await self.moa_generate(problem, entry_point, models=self.llm_dict.values())
            return new_solution['solution'], self.get_cost()

if __name__ == "__main__":
    import asyncio
    from metagpt.ext.aflow.benchmark.humaneval import HumanEvalBenchmark

    async def main():
        graph = MoaAflowWorkflow(name="Moa", llm_names=llm_name_list, dataset="HumanEval")
        benchmark = HumanEvalBenchmark(
            name="HumanEval", 
            file_path="metagpt/ext/aflow/data/humaneval_incremental.jsonl", 
            log_path=""
        )
        avg_score, avg_cost, total_cost = await benchmark.baseline_evaluation(graph, max_concurrent_tasks=5)
        return avg_score, avg_cost, total_cost

    async def single_task():
        graph = MoaAflowWorkflow(name="Moa", llm_names=llm_name_list, dataset="HumanEval")
        task = "\ndef sort_array(arr):\n    \"\"\"\n    In this Kata, you have to sort an array of non-negative integers according to\n    number of ones in their binary representation in ascending order.\n    For similar number of ones, sort based on decimal value.\n\n    It must be implemented like this:\n    >>> sort_array([1, 5, 2, 3, 4]) == [1, 2, 3, 4, 5]\n    >>> sort_array([-2, -3, -4, -5, -6]) == [-6, -5, -4, -3, -2]\n    >>> sort_array([1, 0, 2, 3, 4]) [0, 1, 2, 3, 4]\n    \"\"\"\n"
        function_name = "sort_array" 
        solution, cost = await graph(task, function_name)
        print(solution)
        print(cost)

    async def single_task_test():
        graph = MoaAflowTestWorkflow(name="MoaTest", llm_names=llm_name_list, dataset="HumanEval")
        task = "\ndef sort_array(arr):\n    \"\"\"\n    In this Kata, you have to sort an array of non-negative integers according to\n    number of ones in their binary representation in ascending order.\n    For similar number of ones, sort based on decimal value.\n\n    It must be implemented like this:\n    >>> sort_array([1, 5, 2, 3, 4]) == [1, 2, 3, 4, 5]\n    >>> sort_array([-2, -3, -4, -5, -6]) == [-6, -5, -4, -3, -2]\n    >>> sort_array([1, 0, 2, 3, 4]) [0, 1, 2, 3, 4]\n    \"\"\"\n"
        function_name = "sort_array" 
        solution, cost = await graph(task, function_name)
        print(solution)
        print(cost)

    asyncio.run(single_task_test())
    # score, cost, total_cost = asyncio.run(main())
    # print(f"Moa: {score}, {cost}, {total_cost}")
