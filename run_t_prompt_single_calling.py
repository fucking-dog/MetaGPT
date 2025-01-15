from typing import List, Tuple
from pydantic import BaseModel, Field
from metagpt.configs.models_config import ModelsConfig
from metagpt.ext.aflow.benchmark.hotpotqa import HotpotQABenchmark
from metagpt.ext.aflow.benchmark.mbpp import MBPPBenchmark
from metagpt.ext.aflow.scripts.operator import Operator
from metagpt.ext.aflow.scripts.workflow import Workflow
from metagpt.llm import LLM
import json

def load_tasks_from_jsonl(file_path: str):
    tasks = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():  # 跳过空行
                task = json.loads(line)
                tasks.append(task)
    return tasks

"""
{
    "prompt": "",
    "model": ["gpt-4o-mini"],
    "input_args": ["question", "entry_point"],
    "schema": "SingleGenerateOp",
    "output_args": "solution",
    "dataset": "HotpotQA"
}

"""

class SingleGenerateOp(BaseModel):
    solution: str = Field(default="", description="Solution for the given question.")

class QaGenerateOp(BaseModel):
    thought: str = Field(default="", description="Thought for the given question.")
    solution: str = Field(default="", description="Solution for the given question.")

class SingleTaskWorkflow(Workflow):
    def __init__(self, name: str, llm_config, dataset: str, op: Operator):
        super().__init__(name, llm_config, dataset)
        self.single_op = op
    
    def __call__(self, **input_args):
        response = self.single_op(**input_args)
        return response, self.llm.cost_manager.total_cost

class SingleOperator(Operator):
    def __init__(self, llm: LLM, name: str = "SingleOperator", prompt: str = "", input_args: List[str] = [], output_arg: str = "", schema = ""):
        super().__init__(llm, name)
        self.prompt = prompt
        self.input_args = input_args
        self.output_arg = output_arg

    async def __call__(self, **input_args) -> Tuple[str, str]:
        prompt = self.prompt.format(**input_args)
        response = await self._fill_node(self.schema, prompt, mode="xml_fill")
        return response[self.output_arg]

class TaskRunner:
    def __init__(self, llm_config, schema_dict):
        self.llm_config = llm_config
        self.schema_dict = schema_dict
    
    def get_operator(self, prompt, input_args, schema, output_arg):
        schema = self.schema_dict[schema]
        return SingleOperator(llm=self.llm_config, prompt=prompt, input_args=input_args, schema=schema, output_arg=output_arg)
    
    async def run_single_task(self, task, benchmark):
        operator = self.get_operator(schema=task["schema"], prompt=task["prompt"], input_args=task["input_args"])
        workflow = SingleTaskWorkflow(name="SingleTask", llm_config=self.llm_config, dataset=task["dataset"], op=operator)
        score, cost = benchmark.baseline_evaluation(workflow, max_concurrent_tasks=5)
        return score, cost

if __name__ == "__main__":
    async def main():
        # 配置 LLM
        llm_config = ModelsConfig.default().get("gpt-4o-mini")
        
        # 定义 schema 字典
        schema_dict = {
            "SingleGenerateOp": SingleGenerateOp,
            "QaGenerateOp": QaGenerateOp
        }
        
        # 初始化任务运行器
        runner = TaskRunner(llm_config, schema_dict)
        
        # 加载任务
        tasks = load_tasks_from_jsonl("/path/to/your/tasks.jsonl")
        
        #自定义Benchmark
        benchmark = HotpotQABenchmark(
            name="HotpotQA",
            file_path="metagpt/ext/aflow/data/hotpot_qa_test.jsonl",
            log_path=""
        )
        
        # 运行评估
        results = []
        for task in tasks:
            score, cost = await runner.run_single_task(task, benchmark)
            results.append({"score": score, "cost": cost})
        print(results)
    import asyncio
    asyncio.run(main())
    


step_back_prompt = """
Given the following question:
{question}

Please first think about the principles involved in solving this task which could be helpful.
And Then provide a solution step by step for this question.
"""

rephrase_prompt = """
Given the following question:
{question}

Please rephrase the question in a way that is easier to understand, minimizing ambiguity and considering edge cases.
And Then provide a solution step by step for the question.
"""




