import asyncio
from typing import List
import concurrent.futures

import sys
import traceback
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_fixed

from metagpt.ext.eflow.src.abstract import Operator
from metagpt.ext.eflow.src.prompts.op_prompt import GENERATE_PROMPT, SC_ENSEMBLE_PROMPT, AGGREGATE_PROMPT, REFLECTION_ON_PUBLIC_TEST_PROMPT, VISUAL_FEEDBACK_PROMPT, PYTHON_VISUALIZATION_PROMPT
from metagpt.ext.aflow.scripts.utils import extract_test_cases_from_jsonl, test_case_2_test_function
from metagpt.llm import LLM
from metagpt.utils.sanitize import sanitize
from metagpt.ext.eflow.src.utils import run_visualization_code
from metagpt.logs import logger

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


class MOAGenerate(Operator):
    def __init__(self, model: LLM):
        super().__init__(model, "MOAGenerate")
        self.generate_schema = [{"name": "solution", "type": "str", "description": "Your solution for this problem"}]
        self.aggregate_schema = [
            {"name": "thought", "type": "str", "description": "A detailed explanation of your thought process."},
            {"name": "solution", "type": "str", "description": "Your refined, accurate, and comprehensive reply to the problem."},
        ]

    async def __call__(self, problem: str, function_name: str, models: List[LLM] = None):

        prompt = GENERATE_PROMPT.format(problem=problem)
        solutions = ""
        tasks = [
            self._fill_node(
                op_schema=self.generate_schema, prompt=prompt, format="xml_fill", model=model, function_name=function_name
            )
            for model in models
        ]
        responses = await asyncio.gather(*tasks)
        solutions = "".join(f"{response.get('solution', '')}\n\n\n" for response in responses)

        prompt = AGGREGATE_PROMPT.format(question=problem, solutions=solutions)
        response = await self._fill_node(op_schema=self.aggregate_schema, prompt=prompt, format="xml_fill", model=self.default_model)
        return response

class Test(Operator):
    def __init__(self, model: LLM):
        super().__init__(model, "Test")
        self.schema = [{"name": "reflection_and_solution", "type": "str", "description": "Corrective solution for code execution errors or test case failures"}]

    def exec_code(self, solution, entry_point):
        solution = sanitize(code=solution, entrypoint=entry_point)
        test_cases = extract_test_cases_from_jsonl(entry_point, dataset="HumanEval")
                
        fail_cases = []
        for test_case in test_cases:
            test_code = test_case_2_test_function(solution, test_case, entry_point)
            try:
                exec(test_code, globals())
            except AssertionError as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
                with open("tester.txt", "a") as f:
                    f.write("test_error of " + entry_point + "\n")
                error_infomation = {
                    "test_fail_case": {
                        "test_case": test_case,
                        "error_type": "AssertionError",
                        "error_message": str(e),
                        "traceback": tb_str,
                    }
                }
                fail_cases.append(error_infomation)
            except Exception as e:
                with open("tester.txt", "a") as f:
                    f.write(entry_point + " " + str(e) + "\n")
                return {"exec_fail_case": str(e)}
        if fail_cases != []:
            return fail_cases
        else:
            return "no error"

    async def __call__(
        self, problem, solution, entry_point, test_loop: int = 3, model: LLM = None
    ):
        """
        "Test": {
        "description": "Test the solution with test cases, if the solution is correct, return 'no error', if the solution is incorrect, return reflect on the soluion and the error information",
        "interface": "test(problem: str, solution: str, entry_point: str) -> str"
        }
        """
        for _ in range(test_loop):
            result = self.exec_code(solution, entry_point)
            if result == "no error":
                return {"result": True, "solution": solution}
            elif "exec_fail_case" in result:
                result = result["exec_fail_case"]
                prompt = REFLECTION_ON_PUBLIC_TEST_PROMPT.format(
                    problem=problem,
                    solution=solution,
                    exec_pass=f"executed unsuccessfully, error: \n {result}",
                    test_fail="executed unsucessfully",
                )
                response = await self._fill_node(op_schema=self.schema, prompt=prompt, mode="xml_fill", model=model)
                solution = response["reflection_and_solution"]
            else:
                prompt = REFLECTION_ON_PUBLIC_TEST_PROMPT.format(
                    problem=problem,
                    solution=solution,
                    exec_pass="executed successfully",
                    test_fail=result,
                )
                response = await self._fill_node(op_schema=self.schema, prompt=prompt, mode="xml_fill", model=model)
                solution = response["reflection_and_solution"]
        
        result = self.exec_code(solution, entry_point)
        if result == "no error":
            return {"result": True, "solution": solution}
        else:
            return {"result": False, "solution": solution}
        
class MOATest(Operator):
    def __init__(self, model: LLM):
        super().__init__(model, "MOATest")
        self.reflection_schema = [{"name": "reflection_and_solution", "type": "str", "description": "Corrective solution for code execution errors or test case failures"}]
        self.aggregate_schema = [{"name": "thought", "type": "str", "description": "A detailed explanation of your thought process."}, 
                                {"name": "solution", "type": "str", "description": "Your refined, accurate, and comprehensive reply to the problem."}]
    
    def exec_code(self, solution, entry_point):
        solution = sanitize(code=solution, entrypoint=entry_point)
        test_cases = extract_test_cases_from_jsonl(entry_point, dataset="HumanEval")
                
        fail_cases = []
        for test_case in test_cases:
            test_code = test_case_2_test_function(solution, test_case, entry_point)
            try:
                exec(test_code, globals())
            except AssertionError as e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
                with open("tester.txt", "a") as f:
                    f.write("test_error of " + entry_point + "\n")
                error_infomation = {
                    "test_fail_case": {
                        "test_case": test_case,
                        "error_type": "AssertionError",
                        "error_message": str(e),
                        "traceback": tb_str,
                    }
                }
                fail_cases.append(error_infomation)
            except Exception as e:
                with open("tester.txt", "a") as f:
                    f.write(entry_point + " " + str(e) + "\n")
                return {"exec_fail_case": str(e)}
        if fail_cases != []:
            return fail_cases
        else:
            return "no error"

    async def _get_reflections(self, problem, solution, exec_pass, test_fail, models):
        """获取多个模型的反思和改进方案"""
        tasks = []
        for model in models:
            prompt = REFLECTION_ON_PUBLIC_TEST_PROMPT.format(
                problem=problem,
                solution=solution,
                exec_pass=exec_pass,
                test_fail=test_fail
            )
            tasks.append(self._fill_node(
                op_schema=self.reflection_schema,
                prompt=prompt,
                mode="xml_fill",
                model=model
            ))
        responses = await asyncio.gather(*tasks)
        return "".join(f"{response.get('reflection_and_solution', '')}\n\n\n" for response in responses)

    async def _aggregate_solutions(self, problem, solutions):
        """聚合多个模型的解决方案"""
        prompt = AGGREGATE_PROMPT.format(
            question = "Given a code problem and a python code solution which failed to pass test or execute, you need to analyze the reason for the failure and propose a better code solution.: " + problem, 
            solutions=solutions
        )
        response = await self._fill_node(
            op_schema=self.aggregate_schema,
            prompt=prompt,
            mode="xml_fill",
            model=self.default_model
        )
        return response["solution"]

    async def __call__(
        self, problem, solution, entry_point, test_loop: int = 3, models: List[LLM] = None
    ):
        """
        "Test": {
        "description": "Test the solution with test cases, if the solution is correct, return 'no error', if the solution is incorrect, return reflect on the soluion and the error information",
        "interface": "test(problem: str, solution: str, entry_point: str) -> str"
        }
        """
        for _ in range(test_loop):
            result = self.exec_code(solution, entry_point)
            if result == "no error":
                return {"result": True, "solution": solution}
            
            if "exec_fail_case" in result:
                exec_pass = f"executed unsuccessfully, error: \n {result['exec_fail_case']}"
                test_fail = "executed unsucessfully"
            else:
                exec_pass = "executed successfully"
                test_fail = result

            solutions = await self._get_reflections(problem, solution, exec_pass, test_fail, models)
            solution = await self._aggregate_solutions(problem, solutions)
        
        result = self.exec_code(solution, entry_point)
        return {"result": result == "no error", "solution": solution}
    

class VisualFeedback(Operator):
    def __init__(self, model: LLM):
        super().__init__(model, "VisualFeedback")
        self.schema = [
            {"name": "thought", "type": "str", "description": "The step by step thinking process"},
            {"name": "Feedback", "type": "str", "description": "Visual feedback for the visulizations"}
        ]

    async def __call__(self, query: str, image_path: str, model: LLM = None):
        prompt = VISUAL_FEEDBACK_PROMPT.format(query=query)
        response = await self._fill_node(
            op_schema=self.schema,
            prompt=prompt,
            mode="xml_fill",
            model=model,
            images=[image_path]
        )
        return response["Feedback"]
    
class VisualizationProgrammer(Operator):
    def __init__(self, model:LLM):
        super().__init__(model, "VisualizationProgrammer")
        self.code_generate_schema = [
            {"name": "thought", "type": "str", "description": "The step by step thinking process"},
            {"name": "code", "type": "str", "description": "Your complete code solution for this problem"}
        ]

    async def exec_code(self, code, timeout=60):
        """
        Asynchronously execute code and return an error if timeout occurs.
        """
        loop = asyncio.get_running_loop()
        with concurrent.futures.ProcessPoolExecutor(max_workers=1) as executor:
            try:
                # Submit run_code task to the process pool
                future = loop.run_in_executor(executor, run_visualization_code, code)
                # Wait for the task to complete or timeout
                result = await asyncio.wait_for(future, timeout=timeout)
                return result
            except asyncio.TimeoutError:
                # Timeout, attempt to shut down the process pool
                executor.shutdown(wait=False, cancel_futures=True)
                return "Error", "Code execution timed out"
            except Exception as e:
                return "Error", f"Unknown error: {str(e)}"

    async def code_generate(self, query, analysis, feedback:str, csv_file:str=None, file_path:str=None):
        prompt = PYTHON_VISUALIZATION_PROMPT.format(query=query, analysis=analysis, feedback=feedback, csv_file=csv_file, file_path=file_path)
        response = await self._fill_node(op_schema=self.code_generate_schema, prompt=prompt, mode="xml_fill")
        response["code"] = sanitize(code=response["code"], entrypoint="visualize")
        return response

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def __call__(self, query: str, analysis: str = "None", csv_file:str=None, file_path:str=None):
        """
        Call method, generate code and execute, retry up to 3 times.
        """
        code = None
        output = None
        feedback = ""
        for i in range(3):
            code_response = await self.code_generate(query, analysis, feedback, csv_file=csv_file, file_path=file_path)
            code = code_response.get("code")
            if not code:
                return {"code": code, "visualization_path": "No visualization generated"}
            status, output = await self.exec_code(code)
            if status == "Success":
                return {"code": code, "visualization_path": output}
            else:
                logger.info(f"Execution error on attempt {i + 1}, error message: {output}")
                feedback = (
                    f"\nThe result of the error from the code you wrote in the previous round:\n"
                    f"Code: {code}\n\nStatus: {status}, {output}"
                )
        return {"code": code, "visualization_path": output}
