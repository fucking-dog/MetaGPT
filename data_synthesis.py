from metagpt.ext.eflow.src.abstract import Workflow
from metagpt.ext.eflow.src.operators import Custom, Test, CodeGenerate

llm_name_list = ["gpt-4o-mini"]

IMPROVE_CODE_PROMPT = """
The previous solution failed some test cases. Please analyze the problem carefully and provide an improved solution that addresses all edge cases and requirements. Ensure your code is efficient and follows best practices.
"""

class GeneralWorkflow(Workflow):
    def __init__(
        self,
        name: str,
        llm_names: list,
        dataset: str,
    ) -> None:
        super().__init__(name, llm_names, dataset)
        self.custom = Custom(self.llm_dict["gpt-4o-mini"])
        self.test = Test(self.llm_dict["gpt-4o-mini"])
        self.code_generate = CodeGenerate(self.llm_dict["gpt-4o-mini"])

    async def __call__(self, problem: str, entry_point: str):
        solution = await self.code_generate(problem, entry_point)
        test_result = await self.test(problem=problem, solution=solution['solution'], entry_point=entry_point)
        
        if test_result['result']:
            return test_result['solution'], self.get_cost()
        else:
            # If the test fails, try to generate a new solution with MOA
            problem = problem + "\n" + IMPROVE_CODE_PROMPT
            new_solution = await self.code_generate(problem, entry_point)
            return new_solution['solution'], self.get_cost()
        

class OptimizedWorkflow(Workflow):
    def __init__(
        self,
        name: str,
        llm_names: list,
        dataset: str,
    ) -> None:
        super().__init__(name, llm_names, dataset)
        self.custom = Custom(self.llm_dict["gpt-4o-mini"])
        self.test = Test(self.llm_dict["gpt-4o-mini"])
        self.code_generate = CodeGenerate(self.llm_dict["gpt-4o-mini"])

    async def __call__(self, problem: str, entry_point: str):
        """
        Implementation of the MOA workflow
        """
        solution = await self.code_generate(problem, entry_point)
        test_result = await self.test(problem=problem, solution=solution['solution'], entry_point=entry_point)
        
        for _ in range(3):
            if test_result['result']:
                return test_result['solution'], self.get_cost()
            
            problem = problem + "\n" + IMPROVE_CODE_PROMPT
            new_solution = await self.code_generate(problem, entry_point)
            test_result = await self.test(problem=problem, solution=new_solution['solution'], entry_point=entry_point)
        
        if test_result['result']:
            return test_result['solution'], self.get_cost()
        return new_solution['solution'], self.get_cost()
        

if __name__ == "__main__":
    import asyncio
    from metagpt.ext.aflow.benchmark.humaneval import HumanEvalBenchmark

    async def main():
        graph = GeneralWorkflow(name="General", llm_names=llm_name_list, dataset="HumanEval")
        benchmark = HumanEvalBenchmark(
            name="HumanEval", 
            file_path="metagpt/ext/aflow/data/humaneval_incremental.jsonl", 
            log_path=""
        )
        avg_score, avg_cost, total_cost = await benchmark.baseline_evaluation(graph, max_concurrent_tasks=15)
        return avg_score, avg_cost, total_cost

    async def opt_main():
        graph = OptimizedWorkflow(name="Optimized", llm_names=llm_name_list, dataset="HumanEval")
        benchmark = HumanEvalBenchmark(
            name="HumanEval", 
            # file_path="metagpt/ext/aflow/data/humaneval_incremental.jsonl", 
            file_path="humaneval_vis.jsonl",
            log_path=""
        )
        avg_score, avg_cost, total_cost = await benchmark.baseline_evaluation(graph, max_concurrent_tasks=1)
        return avg_score, avg_cost, total_cost
    
    # score, cost, total_cost = asyncio.run(main())
    # print(f"General: {score}, {cost}, {total_cost}")
    score, cost, total_cost = asyncio.run(opt_main())
    print(f"Optimized: {score}, {cost}, {total_cost}")