# -*- coding: utf-8 -*-
# @Date    : 8/23/2024 10:00 AM
# @Author  : all
# @Desc    : evaluate for different dataset
import datetime
import inspect
import os
from typing import Literal
import numpy as np

import pandas as pd
from deepeval.benchmarks import GSM8K
from typing import Literal, List, Tuple, Optional
import json
import re
import asyncio
from tqdm.asyncio import tqdm_asyncio
import aiofiles

from examples.ags.benchmark.gsm8k import GraphModel

# TODO 完成实验数据集的手动划分

DatasetType = Literal["HumanEval", "MBPP", "Gsm8K", "MATH", "HotpotQA", "MMLU"]


class Evaluator:
    """
    在这里完成对不同数据集的评估
    """

    def __init__(self, eval_path: str):
        self.eval_path = eval_path
        

    def validation_evaluate(self, dataset: DatasetType, graph, params: dict):
        """
        Evaluates on validation dataset.
        """
        if dataset == "Gsm8K":
            return self._gsm8k_eval(graph, params)
        elif dataset == "HumanEval":
            return self._humaneval_eval(graph, params)
        elif dataset == "HotpotQA":
            return self._hotpotqa_eval(graph, params)

    def test_evaluate(self, dataset: DatasetType):
        """
        Evaluates on test dataset.
        """
        pass

    async def _gsm8k_eval(self, graph_class, params, path, test = False):
        """
        Evaluate on GSM8K dataset.
        """

        # 模拟加载模型的函数
        async def load_graph():
            dataset = params["dataset"]
            llm_config = params["llm_config"]

            graph = graph_class(name="Gsm8K", llm_config=llm_config, dataset=dataset)
            return graph

        # 清理文本并提取单个数字
        def extract_number(text: str) -> Optional[float]:
            # 使用正则表达式提取数字，包括整数和浮点数
            matches = re.findall(r"[-+]?\d+(?:,\d{3})*(?:\.\d+)?|\d+\.\d+", text)
            print(matches)
            if matches:
                # 获取最后一个匹配的数字
                last_number = matches[-1]

                # 移除逗号以统一格式
                last_number = last_number.replace(',', '')

                try:
                    return float(last_number)
                except ValueError:
                    return None
            else:
                return None

        # 宽松匹配分数计算函数
        def loose_match_score(expected_output: str, prediction: str, tolerance: float = 1e-6) -> int:
            expected_number = extract_number(expected_output)
            predicted_number = extract_number(prediction)

            print(predicted_number)

            # 如果预期输出或预测输出为空，返回不匹配
            if expected_number is None or predicted_number is None:
                return 0

            # 比较两个提取出的数字，允许一定的容差
            if abs(expected_number - predicted_number) <= tolerance:
                return 1  # 数字相近，认为匹配成功
            else:
                return 0  # 数字不匹配

        # 异步评估单个问题
        async def _evaluate_problem(input: str, graph, expected_output: str) -> Tuple[
            str, str, str, int]:
            prompt = input
            max_retries = 5
            retries = 0

            while retries < max_retries:
                try:
                    # 假设模型有一个异步生成函数
                    prediction = await graph(prompt) if graph else "None"  # 这是一个占位符，替换成实际的模型生成逻辑
                    print(type(prediction))
                    print("预测", prediction)

                    score = loose_match_score(expected_output, prediction[0]['content'])
                    break

                except Exception as e:
                    retries += 1
                    print(f"Error generating prediction: {e}. Retrying... ({retries}/{max_retries})")

                    if retries == max_retries:
                        print("Maximum retries reached. Skipping this sample.")
                        prediction = None
                        score = 0
                        break

            return input, prediction, expected_output, score

        # 异步读取JSONL文件
        async def load_data(file_path: str) -> List[dict]:
            data = []
            async with aiofiles.open(file_path, mode='r') as file:
                async for line in file:
                    data.append(json.loads(line))
            if test:
                # latter 4/5
                data = data[len(data)//5*4:]
            else:
                # former 1/5
                data = data[:len(data)//5*4]
            return data

        # 并行评估所有问题
        async def evaluate_all_problems(data: List[dict], graph, max_concurrent_tasks: int = 50):
            semaphore = asyncio.Semaphore(max_concurrent_tasks)

            async def sem_evaluate(problem):
                async with semaphore:
                    input_text = problem['question']
                    expected_output = problem['answer']
                    return await _evaluate_problem(input_text, graph, expected_output)

            tasks = [sem_evaluate(problem) for problem in data]

            # 使用tqdm.gather来显示进度条
            return await tqdm_asyncio.gather(*tasks, desc="Evaluating problems", total=len(data))

        # 保存结果到CSV文件
        def save_results_to_csv(results: List[Tuple[str, str, str, int]], path):
            df = pd.DataFrame(results, columns=["question", "prediction", "expected_output", "score"])
            average_score = df["score"].mean()

            # 生成文件名，保留五位小数
            output_file = f"{path}/{average_score:.5f}.csv"
            df.to_csv(output_file, index=False)
            print(f"Results saved to {output_file}")

            return average_score

        async def gsm8k():

            file_path = 'examples/ags/w_action_node/data/gsm8k.jsonl'  # 替换为您的JSONL文件路径
            data = await load_data(file_path)

            graph = await load_graph()

            results = await evaluate_all_problems(data, graph, max_concurrent_tasks=20)

            # 保存结果到CSV文件并获取平均分
            average_score = save_results_to_csv(results, path=path)

            print(f"Average score: {average_score:.5f}")
            return average_score

        score = await gsm8k()

        return score

    async def _humaneval_eval(self, graph_class, params, test = False):
        """
        Evaluate on HumanEval dataset.
        """
        
        PASS = "pass"
        FAIL = "fail"
        TIMEOUT = "timeout"

        _SUCCESS = 0
        _FAILED = 1
        _TIMEOUT = 2
        _UNKNOWN = 3

        _mapping = {_SUCCESS: PASS, _FAILED: FAIL, _TIMEOUT: TIMEOUT, _UNKNOWN: None}


        async def load_graph():
            dataset = params["dataset"]
            llm_config = params["llm_config"]

            graph = graph_class(name="HumanEval", llm_config=llm_config, dataset=dataset)
            return graph
        
        async def process_data(data: List[dict]):
            import ast
            prompt = data["prompt"]

            requirements = {}
            requirements["entry_point"] = data["entry_point"]

            async def extract_tests(test_code):
                tree = ast.parse(test_code)
                tests = []

                for node in ast.walk(tree):
                    if isinstance(node, ast.Assert):
                        test = {}
                        test['input'] = [ast.literal_eval(node.test.left.args[i]) for i in range(len(node.test.left.args))]
                        test['expected_output'] = ast.literal_eval(node.test.comparators[0])
                        tests.append(test)

                return tests
            
            requirements["inputs"] = [test['input'] for test in await extract_tests(data["test"])]
            requirements["expected"] = [test['expected_output'] for test in await extract_tests(data["test"])]
            return prompt, requirements


        async def load_data(file_path: str) -> List[dict]:
            data = []
            async with aiofiles.open(file_path, mode='r') as file:
                async for line in file:
                    data.append(json.loads(line))
            if test:
                # latter 4/5
                data = data[len(data)//5*4:]
            else:  
                # former 1/5
                data = data[:len(data)//5*4]
            return data
        
        # oracle for HumaneEval/032
        def _poly(xs: list, x: float):
            """
            Evaluates polynomial with coefficients xs at point x.
            return xs[0] + xs[1] * x + xs[1] * x^2 + .... xs[n] * x^n
            """
            import math
            return sum([coeff * math.pow(x, i) for i, coeff in enumerate(xs)])
        
        def is_floats(x) -> bool:
            # check if it is float; List[float]; Tuple[float]
            if isinstance(x, float):
                return True
            if isinstance(x, (list, tuple)) and x:
                return all(isinstance(i, float) for i in x)
            if isinstance(x, np.ndarray):
                return x.dtype == np.float64 or x.dtype == np.float32
            return False
        
        async def _unsafe_execute(code: str, inputs, entry_point: str, expected: List, atol = 0) -> List[str]:

            progress = 0
            stat = _UNKNOWN
            details = [False for _ in range(len(inputs))]


            exec_globals = {}
            try:

                exec(code, exec_globals)
                fn = exec_globals[entry_point]

                for i, inp in enumerate(inputs):
                    try:

                        out = fn(*inp)

                        exp = expected[i]
                        exact_match = out == exp

                        if "find_zero" == entry_point:
                            assert abs(_poly(*inp, out)) <= atol
                            continue


                        if atol == 0 and is_floats(exp):
                            atol = 1e-6  # enforce atol for float comparison
                        if not exact_match and atol != 0:
                            # explicitly set rtol=1e-07
                            # to match `np.testing.assert_allclose`'s default values
                            assert type(out) == type(exp)
                            if isinstance(exp, (list, tuple)):
                                assert len(out) == len(exp)
                            assert np.allclose(out, exp, rtol=1e-07, atol=atol)
                        else:
                            assert exact_match
                    except BaseException:
                        details[i] = False
                        progress += 1
                        continue

                    details[i] = True
                    progress += 1
                    
                stat = _SUCCESS
            except BaseException:
                stat = _FAILED


            return stat, progress, details

        async def _untrusted_check(code: str, inputs: List, entry_point: str, expected, atol = 0):
            stat, progress, details = await _unsafe_execute(code, inputs, entry_point, expected, atol)

            stat = _mapping[stat]
            details = details[:progress]

            if not stat:
                stat = TIMEOUT

            if stat == PASS:
                if len(details) != len(inputs) or not all(details):
                    stat = FAIL

            return stat, details

        async def _evaluate_problem(input: str, graph, requirements: dict):
            max_retries = 5
            retries = 0

            while retries < max_retries:
                try:
                    solution = await graph(input) if graph else "None"  
                    ret = await _untrusted_check(solution, requirements["inputs"], requirements["entry_point"], requirements["expected"])
                
                    score = 1 if ret[0] == PASS else 0
                    break
                except Exception as e:
                    retries += 1
                    print(f"Error generating prediction: {e}. Retrying... ({retries}/{max_retries})")

                    if retries == max_retries:
                        print("Maximum retries reached. Skipping this sample.")
                        prediction = None
                        score = 0
                        break

            return input, solution, ret[1], score
        
        async def evaluate_all_problems(data: List[dict], graph, requirements: dict, max_concurrent_tasks: int = 50):
            semaphore = asyncio.Semaphore(max_concurrent_tasks)

            async def sem_evaluate(problem):
                async with semaphore:
                    input_text, requirements = await process_data(problem)
                    return await _evaluate_problem(input_text, graph, requirements)

            tasks = [sem_evaluate(problem) for problem in data]

            return await tqdm_asyncio.gather(*tasks, desc="Evaluating problems", total=len(data))
        
        def save_results_to_jsonl(results: List[Tuple[str, str, str, int]], path):
            avg_score = 0
            
            with open(path, "w") as f:
                for result in results:
                    f.write(json.dumps({"question": result[0], "prediction": result[1], "test_case_details": result[2], "score": result[3]}) + "\n")
                    avg_score += result[3]
            print(f"Results saved to {path}")
            avg_score /= len(results)
            
            return avg_score
        
        async def humaneval():
            file_path = 'examples/ags/w_action_node/data/humaneval.jsonl'
            data = await load_data(file_path)

            graph = await load_graph()

            results = await evaluate_all_problems(data, graph, max_concurrent_tasks=20)

            # 保存结果到JSONL文件并获取平均分
            average_score = save_results_to_jsonl(results, path=self.eval_path)

            print(f"Average score: {average_score:.5f}")
            return average_score
        
        score = await humaneval()

        return score


    async def _hotpotqa_eval(self, graph_class, params, test = False):
        """
        Evaluate on HotpotQA dataset.
        """
        def normalize_answer(s):
            import re, string

            def remove_articles(text):
                return re.sub(r'\b(a|an|the)\b', ' ', text)

            def white_space_fix(text):
                return ' '.join(text.split())

            def remove_punc(text):
                exclude = set(string.punctuation)
                return ''.join(ch for ch in text if ch not in exclude)

            def lower(text):
                return text.lower()

            return white_space_fix(remove_articles(remove_punc(lower(s))))

        def exact_match_score(prediction, ground_truth):
            return int(normalize_answer(prediction) == normalize_answer(ground_truth))

        async def load_graph():
            dataset = params["dataset"]
            llm_config = params["llm_config"]

            graph = graph_class(name="HotpotQA", llm_config=llm_config, dataset=dataset)
            return graph
        
        async def load_data(file_path: str) -> List[dict]:
            data = []
            async with aiofiles.open(file_path, mode='r') as file:
                async for line in file:
                    data.append(json.loads(line))
            if test:
                # latter 4/5
                data = data[len(data)//5*4:]
            else:
                # former 1/5
                data = data[:len(data)//5*4]
            return data
        
        async def _evaluate_problem(input: str, context_str: str, graph, expected_output: str):
            max_retries = 5
            retries = 0

            while retries < max_retries:
                try:
                    # TODO Hotpotqa Graph 需要修改输入和输出
                    prediction, supporting_sentences = await graph(input, context_str) if graph else "None"
                    score = exact_match_score(expected_output, prediction[0]['content'])
                    break
                except Exception as e:
                    retries += 1
                    print(f"Error generating prediction: {e}. Retrying... ({retries}/{max_retries})")

                    if retries == max_retries:
                        print("Maximum retries reached. Skipping this sample.")
                        prediction = None
                        score = 0
                        break

            return input, prediction, expected_output, supporting_sentences, score
        
        async def evaluate_all_problems(data: List[dict], graph, max_concurrent_tasks: int = 50):
            semaphore = asyncio.Semaphore(max_concurrent_tasks)

            async def sem_evaluate(problem):
                async with semaphore:
                    input_text = problem['question']
                    expected_output = problem['answer']
                    paragraphs = [item[1] for item in problem["context"] if isinstance(item[1], list)]
                    context_str = "\n".join(" ".join(paragraph) for paragraph in paragraphs)
                    return await _evaluate_problem(input_text, context_str, graph, expected_output)

            tasks = [sem_evaluate(problem) for problem in data]

            return await tqdm_asyncio.gather(*tasks, desc="Evaluating problems", total=len(data))

        def save_results_to_jsonl(results: List[Tuple[str, str, str, str, int]], path):
            avg_score = 0
            
            with open(path, "w") as f:
                for result in results:
                    f.write(json.dumps({"question": result[0], "prediction": result[1], "expected_output": result[2], "supporting_sentences": result[3], "score": result[4]}) + "\n")
                    avg_score += result[4]
            print(f"Results saved to {path}")
            avg_score /= len(results)
            
            return avg_score
        
        async def hotpotqa():
            file_path = 'examples/ags/w_action_node/data/hotpotqa.jsonl'  # 替换为您的JSONL文件路径
            data = await load_data(file_path)

            graph = await load_graph()

            results = await evaluate_all_problems(data, graph, max_concurrent_tasks=20)

            # 保存结果到JSONL文件并获取平均分
            average_score = save_results_to_jsonl(results, path=self.eval_path)

            print(f"Average score: {average_score:.5f}")
            return average_score
        
        score = await hotpotqa()

        return score
        