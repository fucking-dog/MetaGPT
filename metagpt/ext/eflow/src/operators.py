from typing import List

from pydantic import BaseModel, Field

from metagpt.ext.eflow.src.abstract import Operator
from metagpt.ext.eflow.src.prompt import GENERATE_PROMPT, SC_ENSEMBLE_PROMPT
from metagpt.llm import LLM

# Schema List[{name: str, type: str, description: str}]
# # 看起来Schema 需要一个单独的Class，方便进行生成
# 这里的抽象太乱了
# 多LLM应该在调用的时候出现，而不是在Workflow创建的时候出现
# 应该放开Node调整的条件，还是放开Operator的条件？


class Custom(Operator):
    def __init__(self, model: LLM):
        super().__init__(model, "Custom")
        self.schema = [{"name": "response", "type": "str", "description": "Your solution for this problem"}]

    async def __call__(self, input: str, prompt: str, op_schema: BaseModel = None, model: LLM = None, **extra_kwargs):
        if op_schema is None:
            op_schema = self.schema
        context = prompt + input
        response = await self._fill_node(op_schema=op_schema, prompt=context, model=model, **extra_kwargs)
        return response


class CodeGenerate(Operator):
    def __init__(self, model: LLM):
        super().__init__(model, "CodeGenerate")
        self.schema = [{"name": "solution", "type": "str", "description": "Your solution for this problem"}]

    async def __call__(self, problem: str, function_name: str, model: LLM = None):
        prompt = GENERATE_PROMPT.format(problem=problem)
        response = await self._fill_node(
            op_schema=self.schema, prompt=prompt, format="xml_fill", model=model, function_name=function_name
        )
        return response


class ScEnsemble(Operator):
    def __init__(self, model: LLM):
        super().__init__(model, "ScEnsemble")
        self.schema = [
            {"name": "thought", "type": "str", "description": "The thought of the most consistent solution."},
            {"name": "solution_letter", "type": "str", "description": "The letter of most consistent solution."},
        ]

    async def __call__(self, solutions: List[str], problem: str, model: LLM = None):
        answer_mapping = {}
        solution_text = ""
        for index, solution in enumerate(solutions):
            answer_mapping[chr(65 + index)] = index
            solution_text += f"{chr(65 + index)}: \n{str(solution)}\n\n\n"

        prompt = SC_ENSEMBLE_PROMPT.format(question=problem, solutions=solution_text)
        response = await self._fill_node(op_schema=self.schema, prompt=prompt, format="xml_fill", model=model)

        answer = response.get("solution_letter", "")
        answer = answer.strip().upper()

        return {"response": solutions[answer_mapping[answer]]}
