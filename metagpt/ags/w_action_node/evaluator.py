# -*- coding: utf-8 -*-
# @Date    : 8/23/2024 10:00 AM
# @Author  : all
# @Desc    : evaluate for different dataset
import datetime
import inspect
import multiprocessing
import os
import regex
from typing import Literal, List, Tuple, Optional, Union
import re
import pandas as pd
import json
import aiofiles
import asyncio
from tqdm.asyncio import tqdm_asyncio
from math import isclose
from sympy import simplify, N
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.latex import parse_latex


# TODO 完成实验数据集的手动划分

DatasetType = Literal["HumanEval", "MMBP", "Gsm8K", "MATH", "HotpotQa", "MMLU"]


class Evaluator:
    """
    在这里完成对不同数据集的评估
    """

    def __init__(self, eval_path: str):
        self.eval_path = eval_path

    def validation_evaluate(self, dataset: DatasetType, graph, params: dict, path):
        """
        Evaluates on validation dataset.
        """
        if dataset == "Gsm8K":
            score = self._gsm8k_eval(graph, params, path)
            return score
        elif dataset == "MATH":
            score = self._math_eval(graph, params, path)
            return score
        pass

    def test_evaluate(self, dataset: DatasetType):
        """
        Evaluates on test dataset.
        """
        pass

    async def _gsm8k_eval(self, graph_class, params, path, samples: int = 264):
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
            str, str, str, int, str]:
            prompt = input
            max_retries = 5
            retries = 0

            while retries < max_retries:
                try:
                    # 假设模型有一个异步生成函数
                    prediction = await graph(prompt) if graph else "None"  # 这是一个占位符，替换成实际的模型生成逻辑
                    cost = prediction[1]
                    output = prediction[0]['solution']

                    score = loose_match_score(expected_output, prediction[0]['solution'])
                    break

                except Exception as e:
                    retries += 1
                    print(f"Error generating prediction: {e}. Retrying... ({retries}/{max_retries})")

                    if retries == max_retries:
                        print("Maximum retries reached. Skipping this sample.")
                        output = None
                        cost = None
                        score = 0
                        break

            return input, output, expected_output, score, cost

        # 异步读取JSONL文件
        async def load_data(file_path: str) -> List[dict]:
            data = []
            async with aiofiles.open(file_path, mode='r') as file:
                async for line in file:
                    data.append(json.loads(line))
            return data[samples:]

        # 并行评估所有问题
        async def evaluate_all_problems(data: List[dict], graph, max_concurrent_tasks: int = 300):
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
            df = pd.DataFrame(results, columns=["question", "prediction", "expected_output", "score", "cost"])
            average_score = df["score"].mean()

            # 生成文件名，保留五位小数
            output_file = f"{path}/{average_score:.5f}.csv"
            df.to_csv(output_file, index=False)
            print(f"Results saved to {output_file}")

            return average_score

        async def gsm8k():

            file_path = 'metagpt/ags/w_action_node/data/gsm8k.jsonl'  # 替换为您的JSONL文件路径
            data = await load_data(file_path)

            graph = await load_graph()

            results = await evaluate_all_problems(data, graph, max_concurrent_tasks=1)

            # 保存结果到CSV文件并获取平均分
            average_score = save_results_to_csv(results, path=path)

            print(f"Average score: {average_score:.5f}")
            return average_score

        score = await gsm8k()

        return score

    async def _math_eval(self, graph_class, params, path, samples: int = 5):
        """
        Evaluate on MATH dataset.
        """

        async def load_graph():
            dataset = params["dataset"]
            llm_config = params["llm_config"]

            graph = graph_class(name="MATH", llm_config=llm_config, dataset=dataset)
            return graph

        def extract_answer(text: str) -> str:
            # Look for the answer within \boxed{...}
            boxed_match = re.search(r'\\boxed{(.*?)}', text)
            if boxed_match:
                return boxed_match.group(1)

            # If no \boxed{...}, return the last sentence
            sentences = text.split('.')
            return sentences[-1].strip() if sentences else ""

        def parse_digits(num):
            # format: 234.23 || 23%
            num = regex.sub(',', '', str(num))
            try:
                return float(num)
            except:
                if num.endswith('%'):
                    num = num[:-1]
                    if num.endswith('\\'):
                        num = num[:-1]
                    try:
                        return float(num) / 100
                    except:
                        pass
            return None

        def is_digit(num):
            # paired with parse_digits
            return parse_digits(num) is not None

        def symbolic_equal(a, b):
            def _parse(s):
                for f in [parse_latex, parse_expr]:
                    try:
                        return f(s)
                    except:
                        pass
                return s

            a = _parse(a)
            b = _parse(b)

            try:
                if simplify(a - b) == 0:
                    return True
            except:
                pass

            try:
                if isclose(N(a), N(b), abs_tol=1e-3):
                    return True
            except:
                pass
            return False

        def call_with_timeout(func, *args, timeout=5, **kwargs):
            output_queue = multiprocessing.Queue()
            process_args = args + (output_queue,)
            process = multiprocessing.Process(target=func, args=process_args, kwargs=kwargs)
            process.start()
            process.join(timeout)

            if process.is_alive():
                process.terminate()
                process.join()
                return False

            return output_queue.get()

        def math_equal(prediction: Union[bool, float, str],
                       reference: Union[float, str],
                       include_percentage: bool = True,
                       is_close: bool = True,
                       timeout: bool = False,
                       ) -> bool:
            """
            Exact match of math if and only if:
            1. numerical equal: both can convert to float and are equal
            2. symbolic equal: both can convert to sympy expression and are equal
            """
            if str(prediction) == str(reference):
                return True

            try:  # 1. numerical equal
                if is_digit(prediction) and is_digit(reference):
                    prediction = parse_digits(prediction)
                    reference = parse_digits(reference)
                    # number questions
                    if include_percentage:
                        gt_result = [reference / 100, reference, reference * 100]
                    else:
                        gt_result = [reference]
                    for item in gt_result:
                        try:
                            if is_close:
                                if isclose(item, prediction, abs_tol=1e-3):
                                    return True
                            else:
                                if item == prediction:
                                    return True
                        except Exception:
                            continue
                    return False
            except:
                pass

            if not prediction and prediction not in [0, False]:
                return False

            # 2. symbolic equal
            reference = str(reference).strip()
            prediction = str(prediction).strip()

            if regex.match(r'(\(|\[).+(\)|\])', prediction) is not None and regex.match(r'(\(|\[).+(\)|\])',
                                                                                        reference) is not None:
                pred_parts = prediction[1:-1].split(",")
                ref_parts = reference[1:-1].split(",")
                if len(pred_parts) == len(ref_parts):
                    if all([math_equal(pred_parts[i], ref_parts[i], include_percentage, is_close) for i in
                            range(len(pred_parts))]):
                        return True

            if (prediction.startswith("\\begin{pmatrix}") or prediction.startswith("\\begin{bmatrix}")) and (
                    prediction.endswith("\\end{pmatrix}") or prediction.endswith("\\end{bmatrix}")) and \
                    (reference.startswith("\\begin{pmatrix}") or reference.startswith("\\begin{bmatrix}")) and (
                    reference.endswith("\\end{pmatrix}") or reference.endswith("\\end{bmatrix}")):
                pred_lines = [line.strip() for line in
                              prediction[len("\\begin{pmatrix}"): -len("\\end{pmatrix}")].split("\\\\") if line.strip()]
                ref_lines = [line.strip() for line in
                             reference[len("\\begin{pmatrix}"): -len("\\end{pmatrix}")].split("\\\\") if line.strip()]
                matched = True
                if len(pred_lines) == len(ref_lines):
                    for pred_line, ref_line in zip(pred_lines, ref_lines):
                        pred_parts = pred_line.split("&")
                        ref_parts = ref_line.split("&")
                        if len(pred_parts) == len(ref_parts):
                            if not all([math_equal(pred_parts[i], ref_parts[i], include_percentage, is_close) for i in
                                        range(len(pred_parts))]):
                                matched = False
                                break
                        else:
                            matched = False
                        if not matched:
                            break
                else:
                    matched = False
                if matched:
                    return True

            if prediction.count('=') == 1 and reference.count('=') == 1:
                pred = prediction.split('=')
                pred = f"{pred[0].strip()} - ({pred[1].strip()})"
                ref = reference.split('=')
                ref = f"{ref[0].strip()} - ({ref[1].strip()})"
                if symbolic_equal(pred, ref) or symbolic_equal(f"-({pred})", ref):
                    return True
            elif prediction.count('=') == 1 and len(prediction.split('=')[0].strip()) <= 2 and '=' not in reference:
                if math_equal(prediction.split('=')[1], reference, include_percentage, is_close):
                    return True
            elif reference.count('=') == 1 and len(reference.split('=')[0].strip()) <= 2 and '=' not in prediction:
                if math_equal(prediction, reference.split('=')[1], include_percentage, is_close):
                    return True

            # symbolic equal with sympy
            if timeout:
                if call_with_timeout(symbolic_equal, prediction, reference):
                    return True
            else:
                if symbolic_equal(prediction, reference):
                    return True

            return False

        def calculate_score(expected_output: str, prediction: str) -> int:
            expected_answer = extract_answer(expected_output)
            predicted_answer = extract_answer(prediction)

            return 1 if math_equal(predicted_answer, expected_answer) else 0

        async def _evaluate_problem(problem: dict, graph) -> Tuple[str, str, str, int, str]:
            input_text = problem['problem']
            expected_output = problem['solution']
            max_retries = 5
            retries = 0

            while retries < max_retries:
                try:
                    prediction = await graph(input_text) if graph else "None"
                    cost = prediction[1]
                    output = prediction[0]['solution']

                    score = calculate_score(expected_output, output)
                    break

                except Exception as e:
                    retries += 1
                    print(f"Error generating prediction: {e}. Retrying... ({retries}/{max_retries})")

                    if retries == max_retries:
                        print("Maximum retries reached. Skipping this sample.")
                        output = None
                        cost = None
                        score = 0
                        break

            return input_text, output, expected_output, score, cost

        async def load_data(file_path: str) -> List[dict]:
            data = []
            async with aiofiles.open(file_path, mode='r') as file:
                async for line in file:
                    data.append(json.loads(line))
            return data[:samples]

        async def evaluate_all_problems(data: List[dict], graph, max_concurrent_tasks: int = 300):
            semaphore = asyncio.Semaphore(max_concurrent_tasks)

            async def sem_evaluate(problem):
                async with semaphore:
                    return await _evaluate_problem(problem, graph)

            tasks = [sem_evaluate(problem) for problem in data]

            return await tqdm_asyncio.gather(*tasks, desc="Evaluating MATH problems", total=len(data))

        def save_results_to_csv(results: List[Tuple[str, str, str, int]], path):
            df = pd.DataFrame(results, columns=["question", "prediction", "expected_output", "score", "cost"])
            average_score = df["score"].mean()

            output_file = f"{path}/{average_score:.5f}.csv"
            df.to_csv(output_file, index=False)
            print(f"Results saved to {output_file}")

            return average_score

        async def math_evaluation():
            file_path = 'metagpt/ags/w_action_node/data/math.jsonl'  # Replace with the actual path to MATH.jsonl
            data = await load_data(file_path)

            graph = await load_graph()

            results = await evaluate_all_problems(data, graph, max_concurrent_tasks=20)

            average_score = save_results_to_csv(results, path=path)

            print(f"Average score on MATH dataset: {average_score:.5f}")
            return average_score

        score = await math_evaluation()

        return score
