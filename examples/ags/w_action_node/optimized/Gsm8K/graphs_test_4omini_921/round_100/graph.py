from metagpt.actions.action_node import ActionNode
from metagpt.configs.models_config import ModelsConfig
from metagpt.llm import LLM
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Tuple
from collections import Counter
from tenacity import retry, stop_after_attempt, wait_fixed
import traceback
import re
import sys
import random
from typing import Literal

from metagpt.provider.llm_provider_registry import create_llm_instance
from metagpt.utils.cost_manager import CostManager

DatasetType = Literal["HumanEval", "MBPP", "Gsm8K", "MATH", "HotpotQa", "MMLU"]

cost_manager = CostManager()

# TODO 这个类应该作为一个基类，不能够这样使用
class Graph:
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


    async def __call__(self, problem: str):
        """
        Implementation of the graph
        """
        solution = ""
        return solution, self.llm.cost_manager.total_cost

REPHRASE_ON_PROBLEM_PROMPT = """
You are given a code contest problem:

### problem
{problem}

### instrcutions
Given the problem, Your Goal is:
Reflect on the problem, especially focus on the ambiguous brought by some words and then describe it in your own words, in bullet points. Pay attention to small details, language ambiguity, nuances, notes and examples in the problem description.

Example:
After scoring 14 points, Erin now has three times more points than Sara, who scored 8. How many points did Erin have before?
Erin's now points is 32 or 24? It's 32, which is a classic trap for students who are not careful with the problem statement. Your goal is to avoid this trap.
"""
PYTHON_CODE_VERIFIER_PROMPT = """
You are a professional Python programmer. Your task is to write code based on a given mathematical problem and output the answer.

Always provide complete, self-contained code rather than just suggestions or partial modifications. Your code should include all necessary imports and dependencies, and be ready to run without additional setup or environment configuration.

Problem description: {problem}

Your code should:
1. Implement the calculation steps described in the problem
2. Define a function named 'solve' that outputs the result of the calculation
3. Print the final result of the calculation

Please ensure your code is efficient, well-commented, and follows Python best practices.
"""

GSM8K_PROMPT_COT = """
{question}\nPlease reason step by step. At the end, provide the final answer in the format "Answer is <number>", where <number> is a single number, without any additional information or explanation.
"""

SC_ENSEMBLE_PROMPT = """
Given the question described as follows: {question}
Several solutions have been generated to address the given question. They are as follows:
{solutions}

Carefully evaluate these solutions and identify the answer that appears most frequently across them. This consistency in answers is crucial for determining the most reliable solution.

In the "thought" field, provide a detailed explanation of your thought process. In the "solution_letter" field, output only the single letter ID (A, B, C, etc.) corresponding to the most consistent solution. Do not include any additional text or explanation in the "solution_letter" field.
"""

CONTEXTUAL_CHOICE_PROMPT = """
Given a problem and some solutions, based on the problem description and solution's thought or code, think step by step and choose the most appropriate solution.

Please choose the most appropriate solution and output the letter of the solution(Such as A, B, C, D, etc.).
"""


class Operator:
    def __init__(self, name, llm: LLM):
        self.name = name
        self.llm = llm

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

class CodeGenerateOp(BaseModel):
    code: str = Field(default="", description="Your complete code solution for this problem")


class GenerateOp(BaseModel):
    solution: str = Field(default="", description="solution for the problem")


class ChoiceOp(BaseModel):
    thought: str = Field(default="", description="The thought of the most consistent solution.")
    solution: str = Field(default="", description="solution for the problem")


class RephraseOp(BaseModel):
    rephrased_problem: str = Field(default="", description="rephrased problem")


class CoTGenerate(Operator):
    def __init__(self, llm: LLM, name: str = "Generate"):
        super().__init__(name, llm)

    async def __call__(self, problem, mode: str = None):
        prompt = GSM8K_PROMPT_COT.format(question=problem)
        fill_kwargs = {"context": prompt, "llm": self.llm}
        if mode:
            fill_kwargs["mode"] = mode
        node = await ActionNode.from_pydantic(GenerateOp).fill(**fill_kwargs)
        response = node.instruct_content.model_dump()
        return response


class ScEnsembleOp(BaseModel):
    thought: str = Field(default="", description="The thought of the most consistent solution.")
    solution_letter: str = Field(default="", description="The letter of most consistent solution.")


class ScEnsemble(Operator):
    """
    Paper: Self-Consistency Improves Chain of Thought Reasoning in Language Models
    Link: https://arxiv.org/abs/2203.11171
    Paper: Universal Self-Consistency for Large Language Model Generation
    Link: https://arxiv.org/abs/2311.17311
    """

    def __init__(self, name: str = "ScEnsemble", llm: LLM = LLM()):
        super().__init__(name, llm)

    async def __call__(self, solutions: List[str], problem: str, mode: str = None):
        answer_mapping = {}
        solution_text = ""
        for index, solution in enumerate(solutions):
            answer_mapping[chr(65 + index)] = index
            solution_text += f"{chr(65 + index)}: \n{str(solution)}\n\n\n"

        prompt = SC_ENSEMBLE_PROMPT.format(solutions=solution_text, question=problem)
        fill_kwargs = {"context": prompt, "llm": self.llm}
        if mode:
            fill_kwargs["mode"] = mode
        node = await ActionNode.from_pydantic(ScEnsembleOp).fill(**fill_kwargs)
        response = node.instruct_content.model_dump()

        answer = response.get("solution_letter", "A")
        answer = answer.strip().upper()

        return {"solution": solutions[answer_mapping[answer]]}


class Custom(Operator):
    def __init__(self, llm: LLM, name: str = "Custom"):
        super().__init__(name, llm)

    async def __call__(self, input, instruction):
        prompt = input + instruction
        node = await ActionNode.from_pydantic(ChoiceOp).fill(context=prompt, llm=self.llm, mode="context_fill")
        response = node.instruct_content.model_dump()
        return response


class Rephrase(Operator):
    """
    Paper: Code Generation with AlphaCodium: From Prompt Engineering to Flow Engineering
    Link: https://arxiv.org/abs/2404.14963
    Paper: Achieving >97% on GSM8K: Deeply Understanding the Problems Makes LLMs Better Solvers for Math Word Problems
    Link: https://arxiv.org/abs/2404.14963
    """

    def __init__(self, name: str = "Rephrase", llm: LLM = LLM()):
        super().__init__(name, llm)

    async def __call__(self, problem: str, mode: str = "context_fill") -> str:
        prompt = REPHRASE_ON_PROBLEM_PROMPT.format(problem=problem)
        fill_kwargs = {"context": prompt, "llm": self.llm}
        if mode:
            fill_kwargs["mode"] = mode
        node = await ActionNode.from_pydantic(RephraseOp).fill(**fill_kwargs)
        response = node.instruct_content.model_dump()
        return response  # {"rephrased_problem": "xxx"}


class PythonInterpreter(Operator):
    def __init__(self, name: str = "PythonInterpreter", llm: LLM = LLM()):
        super().__init__(name, llm)

    async def exec_code(self, code, timeout=600):
        try:
            # 创建一个新的全局命名空间
            global_namespace = {}

            # 使用exec执行代码
            exec(code, global_namespace)

            # 假设代码中定义了一个名为'solve'的函数
            if 'solve' in global_namespace:
                result = global_namespace['solve']()
                return "Success", str(result)
            else:
                return "Error", "未找到'solve'函数"
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
            return "Error", f"执行错误: {str(e)}\n{''.join(tb_str)}"

    def extract_code_block(self, code_block):
        match = re.search(r"```python(.*?)```", code_block, re.DOTALL)
        if match:
            code = match.group(1)
            return code.encode("utf-8", "ignore").decode("utf-8")
        else:
            return "No code"

    async def code_generate(self, problem, mode):
        prompt = PYTHON_CODE_VERIFIER_PROMPT.format(problem=problem)
        fill_kwargs = {"context": prompt, "llm": self.llm, "function_name": "solve"}
        if mode:
            fill_kwargs["mode"] = mode
        node = await ActionNode.from_pydantic(CodeGenerateOp).fill(**fill_kwargs)
        response = node.instruct_content.model_dump()
        return response

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def __call__(self, problem: str, mode: str = "context_fill"):
        for i in range(3):
            code = await self.code_generate(problem, mode)
            code = self.extract_code_block(code["code"])
            status, output = await self.exec_code(code)

            if status == "Success":
                return {"code": code, "output": output}
            else:
                print(f"第{i + 1}次执行错误，错误信息：{output}")

        return {"code": code, "output": "error"}


class SolveGraph(Graph):
    def __init__(self, name: str, llm_config, dataset: str):
        super().__init__(name, llm_config, dataset)
        self.rephrase = Rephrase(llm=self.llm)
        self.cot_generate = CoTGenerate(llm=self.llm)
        self.sc_ensemble = ScEnsemble(llm=self.llm)
        self.interpreter = PythonInterpreter(llm=self.llm)
        self.custom = Custom(llm=self.llm)

    async def __call__(self, problem):

        rephrased_problem = await self.rephrase(problem)
        rephrased_problem = f"original problem: {problem}\n\nrephrased problem: {rephrased_problem['rephrased_problem']}"

        solutions = []
        solutions_text = []
        for i in range(5):
            solution = await self.cot_generate(problem, mode="context_fill")
            solutions.append(solution)
            solutions_text.append(solution["solution"])
        sc_solution = await self.sc_ensemble(solutions_text, problem, mode="context_fill")

        rephrased_solution = await self.cot_generate(rephrased_problem, mode="context_fill")
        code_solution = await self.interpreter(problem, mode="context_fill")

        sc_solution_desc = f"thought and solution: {sc_solution['solution']}"
        rephrased_solution_desc = f"thought and solution: {rephrased_solution['solution']}"
        code_solution_desc = f"code: {code_solution['code']}\nsolution: {code_solution['output']}"
        if code_solution["output"] == "error":
            solution_description = f"A: {sc_solution_desc}\nB: {rephrased_solution_desc}"
        else:
            solution_description = f"A: {sc_solution_desc}\nB: {rephrased_solution_desc}\nC: {code_solution_desc}"
        final_solution = {"solution": sc_solution["solution"]}
        choice = await self.custom(problem + "\n" + solution_description, CONTEXTUAL_CHOICE_PROMPT)
        if choice["solution"] == "A":
            final_solution = {"solution": sc_solution["solution"]}
        elif choice["solution"] == "B":
            final_solution = {"solution": rephrased_solution["solution"]}
        elif choice["solution"] == "C":
            final_solution = {"solution": code_solution["output"]}
        else:
            final_solution = {"solution": sc_solution["solution"]}

        return final_solution['solution'], self.llm.cost_manager.total_cost


