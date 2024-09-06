# -*- coding: utf-8 -*-
# @Date    : 8/12/2024 22:00 PM
# @Author  : issac
# @Desc    : optimizer for graph

import asyncio
import json
import os
import re
import time
from collections import defaultdict
from typing import List, Literal



import numpy as np
from pydantic import BaseModel, Field
# import sys
# import os
# sys.path.append("/Users/femtozheng/python-project/jinyu")
from metagpt.ags.w_action_node.evaluator import Evaluator
from metagpt.ags.w_action_node.prompts.optimize_prompt import (
    GRAPH_INPUT,
    GRAPH_OPTIMIZE_PROMPT,
    GRAPH_TEMPLATE,
    OPERATOR_INPUT,
    OPERATOR_OPTIMIZE_PROMPT,
    OPERATOR_TEMPLATE,
)
from metagpt.actions.action_node import ActionNode
from metagpt.logs import logger
from metagpt.provider.llm_provider_registry import create_llm_instance

config_iterate_path = "iterate"

DatasetType = Literal["HumanEval", "MMBP", "Gsm8K", "MATH", "HotpotQa", "MMLU"]
OptimizerType = Literal["Complete", "Graph", "Operator"]

class OperatorOptimize(BaseModel):
    pass


class GraphOptimize(BaseModel):
    modification: str = Field(default="", description="modification")
    graph: str = Field(default="", description="graph")
    prompt: str = Field(default="", description="prompt(Only Custom method Prompt)")


class Optimizer:
    def __init__(
        self,
        dataset: DatasetType,
        opt_llm_config,
        exec_llm_config,
        operators: List,
        optimized_path: str = None,
        sample: int = 6,
        q_type: str = "math",  # math,code,quiz
        op: str = "Generator",  # 需要优化的Operator
    ) -> None:
        self.optimize_llm_config = opt_llm_config
        self.execute_llm_config = exec_llm_config
        self.optimize_llm = create_llm_instance(self.optimize_llm_config)
        self.dataset = dataset
        self.graph = None  # 初始化为 None，稍后加载
        self.operators = operators
        self.op = op
        self.optimize_prompt = ""
        self._optimized_path = optimized_path
        self.root_path = f"{self._optimized_path}/{self.dataset}"
        self.sample = sample
        self.score = "None"
        self.top_scores = []
        self.type = q_type
        self.round = 24  # 起始轮次

    def _initialize_oprimizer(self):
        pass

    def _initialize_operator(self):
        # TODO @issac
        pass

    def _initialize(self):
        """
        基于数据集、操作符初始化optimize prompt, operator 跟 graph
        """
        self._initialize_optimizer()

        round_1_path = f"{self.root_path}/graphs/round_1"
        required_files = ["operator.py", "prompt.py"]

        def check_files_exist(basic_path, required_files):
            missing_files = []

            for file in required_files:
                if not os.path.exists(os.path.join(basic_path, file)):
                    missing_files.append(file)

            if not missing_files:
                return True, []
            else:
                return False, missing_files

        if check_files_exist(round_1_path, required_files):
            logger.info(f"{self.dataset} has been initialized")
            return True
        else:
            logger.info(f"{self.dataset} has not been initialized")

        # 迭代优化Operator，Opt可视内容：Prompt，Operator
        self._initialize_operator()

        # 初始化Graph，直接手动从模版中取出（COT）

    def optimize(self, mode: OptimizerType = "Complete", max_rounds: int = 100):
        """
        Optimize the graph and operator for the dataset.
        """
        if mode == "Complete":
            self._initialize()  # Operator's Optimization
        for opt_round in range(max_rounds):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            retry_count = 0
            max_retries = 5
            while retry_count < max_retries:
                try:
                    score = loop.run_until_complete(self._optimize_graph())
                    break  # 如果成功，跳出重试循环
                except Exception as e:
                    retry_count += 1
                    print(f"Error occurred: {e}. Retrying... (Attempt {retry_count}/{max_retries})")
                    if retry_count == max_retries:
                        print("Max retries reached. Moving to next round.")
                        score = None  # 或者设置一个默认分数
                    time.sleep(5)  # 在重试之前等待一段时间
                finally:
                    # 每次尝试后都关闭当前的事件循环
                    loop.close()

                if retry_count < max_retries:
                    # 如果还需要重试，创建新的事件循环
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
            self.round += 1
            print(f"Score for round {self.round}: {score}")
            time.sleep(5)

    def _load_graph(self, round_number, graphs_path):
        """
        动态加载指定轮次的 Graph 类。
        """
        graphs_path = graphs_path.replace("\\", ".").replace("/", ".")
        graph_module_name = f"{graphs_path}.round_{round_number}.graph"

        try:
            graph_module = __import__(graph_module_name, fromlist=[""])
            graph_class = getattr(graph_module, "SolveGraph")
            self.graph = graph_class
        except ImportError as e:
            print(f"Error loading graph for round {round_number}: {e}")
            raise

    def _read_graph_files(self, round_number, graphs_path):
        """
        动态读取指定轮次的 Prompt和Graph。
        """
        # 构建 prompt.py 文件的相对路径
        # examples/ags/w_action_node/optimized/Gsm8k/graphs/round_1
        prompt_file_path = os.path.join(graphs_path, f"round_{round_number}", "prompt.py")
        graph_file_path = os.path.join(graphs_path, f"round_{round_number}", "graph.py")

        try:
            with open(prompt_file_path, "r", encoding="utf-8") as file:
                prompt_content = file.read()
            with open(graph_file_path, "r", encoding="utf-8") as file:
                graph_content = file.read()

        except FileNotFoundError as e:
            print(f"Error: File not found for round {round_number}: {e}")
            raise
        except Exception as e:
            print(f"Error loading prompt for round {round_number}: {e}")
            raise
        return prompt_content, graph_content

    def _load_scores(self):
        rounds_dir = os.path.join(self.root_path, "graphs")
        self.top_scores = []

        # 遍历所有轮次的文件夹
        for round_dir in os.listdir(rounds_dir):
            if os.path.isdir(os.path.join(rounds_dir, round_dir)) and round_dir.startswith("round_"):
                round_number = int(round_dir.replace("round_", ""))
                csv_file_path = os.path.join(rounds_dir, round_dir)
                try:
                    # 遍历文件夹中的文件，查找 CSV 文件
                    for filename in os.listdir(csv_file_path):
                        score = 0

                        if filename.endswith(".csv"):
                            # 文件名就是分数
                            score = float(filename[:-4])  # 去除.csv

                        self.top_scores.append(
                            {
                                "round": round_number,
                                "score": score,
                            }
                        )

                except FileNotFoundError as e:
                    print(f"Error: File not found for round {round_number}: {e}")
                    continue
                except ValueError as e:
                    print(f"Error parsing score from filename for round {round_number}: {e}")
                    continue
                except Exception as e:
                    print(f"Error processing round {round_number}: {e}")
                    continue

        # 对所有轮次的分数进行排序
        self.top_scores.sort(key=lambda x: x["score"], reverse=True)

    def _exponential_decay(self, ranks, alpha=0.3):
        # 根据ranks计算权重
        weights = np.exp(-alpha * ranks)
        # 归一化权重使其总和为1
        prob = weights / np.sum(weights)
        return prob

    def _select_round(self, items):
        # 首先根据'score'字段对items列表进行降序排序
        sorted_items = sorted(items, key=lambda x: x["score"], reverse=True)

        # 提取排序后的位次（从1开始）
        ranks = np.array([i for i in range(1, len(sorted_items) + 1)])

        # 计算概率分布
        probabilities = self._exponential_decay(ranks)

        # 选择一个索引
        selected_index = np.random.choice(len(sorted_items), p=probabilities)

        # 返回选定的条目
        return sorted_items[selected_index]

    def _get_top_rounds(self):
        """
        返回分数最高的 top_x 个轮次，并确保返回的轮次不重复。
        """
        self._load_scores()
        # 创建一个集合来跟踪已包含的轮次
        unique_rounds = set()
        unique_top_scores = []

        # 首先，添加第一轮（轮次 1），如果它存在的话
        first_round = next((item for item in self.top_scores if item["round"] == 1), None)
        if first_round:
            unique_top_scores.append(first_round)
            unique_rounds.add(1)

        # 遍历 top_scores 列表
        for item in self.top_scores:
            if item["round"] not in unique_rounds:
                unique_top_scores.append(item)
                unique_rounds.add(item["round"])

                # 如果已经收集到了足够的唯一轮次，则提前终止循环
                if len(unique_top_scores) == self.sample:
                    break

        return unique_top_scores

    def _load_experience(self):
        rounds_dir = os.path.join(self.root_path, "graphs")
        experience_data = defaultdict(lambda: {"score": None, "success": {}, "failure": {}})

        # 遍历所有轮次的文件夹
        for round_dir in os.listdir(rounds_dir):
            if os.path.isdir(os.path.join(rounds_dir, round_dir)) and round_dir.startswith("round_"):
                round_path = os.path.join(rounds_dir, round_dir)
                try:
                    # 提取轮次的数字
                    round_number = int(round_dir.split("_")[1])

                    # 查找 experience.json 文件
                    json_file_path = os.path.join(round_path, "experience.json")
                    if os.path.exists(json_file_path):
                        with open(json_file_path, "r", encoding="utf-8") as json_file:  # 指定 UTF-8 编码
                            data = json.load(json_file)
                            father_node = data["father node"]

                            # 如果这是该父节点的第一条记录，设置其分数
                            if experience_data[father_node]["score"] is None:
                                experience_data[father_node]["score"] = data["before"]

                            # 根据成功与否，将数据添加到相应的字典中
                            if data["succeed"]:
                                experience_data[father_node]["success"][round_number] = {
                                    "modification": data["modification"],
                                    "score": data["after"]
                                }
                            else:
                                experience_data[father_node]["failure"][round_number] = {
                                    "modification": data["modification"],
                                    "score": data["after"]
                                }
                    else:
                        print(f"experience.json not found for round {round_dir}")
                except Exception as e:
                    print(f"Error processing {round_dir}: {str(e)}")

        # 将 defaultdict 转换为普通 dict
        experience_data = dict(experience_data)

        # 保存为 JSON 文件
        output_path = os.path.join(self.root_path, "graphs", "processed_experience.json")
        with open(output_path, "w", encoding="utf-8") as outfile:  # 指定 UTF-8 编码
            json.dump(experience_data, outfile, indent=4, ensure_ascii=False)  # ensure_ascii=False 以正确保存中文字符

        print(f"Processed experience data saved to {output_path}")
        return experience_data

    def _load_operators_description(self, mode: OptimizerType = "Graph"):
        def _load_operator_description(id, operator_name, file_path):
            """
            针对初始Operator，我们从最外层中读取
            对于修改后的Operator，我们从对应的round中读取
            """
            with open(file_path, "r") as f:
                operator_data = json.load(f)
                matched_data = operator_data[operator_name]
                operator_description = f"{id}. {operator_name}: {matched_data['description']}, with interface {matched_data['interface']})."
                return operator_description
        if mode == "Graph":
            path = f"{self.root_path}/graphs/template/operator.json"
        else:
            path = "examples/ags/data/operator.json"
        operators_description = ""
        for id, operator in enumerate(self.operators):
            operator_description = _load_operator_description(id+1, operator, path)
            operators_description += f"{operator_description}\n"
        return operators_description

    async def _optimize_graph(self):
        """
        Optimize Graph's Structure and Prompt
        """
        try:
            # 获取项目的根目录
            graph_path = f"{self.root_path}/graphs"

            # 创建文件夹（如果不存在）
            directory = os.path.join(graph_path, f"round_{self.round + 1}")
            os.makedirs(directory, exist_ok=True)

            # top_rounds = self._get_top_rounds()
            #
            # sample = self._select_round(top_rounds)
            #
            # print(sample)
            #
            # prompt, graph_load = self._read_graph_files(sample["round"], graph_path)
            # score = sample["score"]
            #
            # # 正则表达式匹配 SolveGraph 开始的内容
            # pattern = r"class SolveGraph:.+"
            #
            # # 使用re.findall找到所有匹配项
            # graph = re.findall(pattern, graph_load, re.DOTALL)
            #
            # # 加载处理过的 experience 数据
            # processed_experience = self._load_experience()
            #
            # # 获取当前轮次的 experience 数据
            # current_round = int(sample["round"])  # 确保是字符串类型
            # experience_data = processed_experience.get(current_round)
            #
            # if experience_data:
            #     # 构建 experience 字符串
            #     experience = f"Original Score: {experience_data['score']}\n"
            #     experience += "Failed modifications:\n"
            #     for key, value in experience_data["failure"].items():
            #         experience += f"- {value['modification']} (Score: {value['score']})\n"
            #     for key, value in experience_data["success"].items():
            #         experience += f"- {value['modification']} \n"
            #     experience += "\n\nNote: Reference failed experiences, avoid trying failed approaches again, attempt to change your thinking, not limited to using more advanced Python syntax like for, if, else, etc., or modifying the Prompt part"
            # else:
            #     experience = f"No experience data found for round {current_round}."
            #
            # operator_description = self._load_operators_description()
            #
            # graph_input = GRAPH_INPUT.format(
            #     experience=experience, score=score, graph=graph[0], prompt=prompt, operator_description=operator_description, type=self.type
            # )
            # graph_system = GRAPH_OPTIMIZE_PROMPT.format(type=self.type)
            #
            # graph_optimize_prompt = graph_system + graph_input  # TODO 看一眼谁先谁后这个地方
            #
            # # TODO 从这里开始，Graph Optimize 可以作为一个Operator放入 Operator.py 之中
            # graph_optimize_node = await ActionNode.from_pydantic(GraphOptimize).fill(
            #     context=graph_optimize_prompt, mode="context_fill", llm=self.optimize_llm
            # )
            #
            # max_retries = 5
            # retries = 0
            #
            # while retries < max_retries:
            #     try:
            #         # TODO 需要和评测的模型分开（传入模型或其它方法），如果能实现Temperature调整更好
            #         response = graph_optimize_node.instruct_content.model_dump()
            #         break
            #
            #     except Exception as e:
            #         retries += 1
            #         print(f"Error generating prediction: {e}. Retrying... ({retries}/{max_retries})")
            #
            #         if retries == max_retries:
            #             print("Maximum retries reached. Skipping this sample.")
            #             break
            #         time.sleep(5)
            #
            # graph_match = response["graph"]
            # prompt = response["prompt"]
            # modification = response["modification"]
            #
            # graph = GRAPH_TEMPLATE.format(graph=graph_match, round=self.round + 1)
            #
            # # 将 graph.py 文件写入到目录中
            # with open(os.path.join(directory, "graph.py"), "w", encoding="utf-8") as file:
            #     file.write(graph)
            #
            # # 将 prompt.py 文件写入到目录中
            # with open(os.path.join(directory, "prompt.py"), "w", encoding="utf-8") as file:
            #     file.write(prompt)
            #
            # # 将 prompt.py 文件写入到目录中
            # with open(os.path.join(directory, "__init__.py"), "w", encoding="utf-8") as file:
            #     file.write("")
            #
            # experience = {
            #     "father node": sample["round"],
            #     "modification": modification,
            #     "before": sample["score"],
            #     "after": None,
            #     "succeed": None,
            # }

            self._load_graph(self.round + 1, graph_path)

            evaluator = Evaluator(eval_path=directory)

            print(self.graph)
            print(self.round)

            score = await evaluator.validation_evaluate(
                self.dataset, self.graph, {"dataset": self.dataset, "llm_config": self.execute_llm_config}, directory
            )
            # experience["after"] = score
            # experience["succeed"] = bool(score > experience["before"])
            #
            # with open(os.path.join(directory, "experience.json"), "w", encoding="utf-8") as file:
            #     json.dump(experience, file, ensure_ascii=False, indent=4)

            return score

        except Exception as e:
            print(f"Error in _optimize_graph: {e}")
            print(f"Current state: {self.__dict__}")  # 打印对象的当前状态
            raise  # 重新抛出异常

    async def _optimize_operator(self):
        """
        Optimize Graph's Structure and Prompt
        """
        # 获取项目的根目录
        graph_path = f"{self.root_path}/operators"

        # 创建文件夹（如果不存在）
        directory = os.path.join(graph_path, f"round_{self.round + 1}")
        os.makedirs(directory, exist_ok=True)

        top_rounds = self._get_top_rounds()

        sample = self._select_round(top_rounds)

        print(top_rounds)

        prompt, graph_load, operator_load = self._read_files(sample["round"])
        score = sample["score"]

        # 正则表达式匹配 SolveGraph 开始的内容
        operator_pattern = rf"class {self.op}(Operator):.+"

        graph_pattern = r"class SolveGraph:.+"

        # 使用re.findall找到所有匹配项
        operator = re.findall(operator_pattern, operator_load, re.DOTALL)
        graph = re.findall(graph_pattern, graph_load, re.DOTALL)

        # 加载处理过的 experience 数据
        processed_experience = self._load_experience()

        # 获取当前轮次的 experience 数据
        current_round = int(sample["round"])  # 确保是字符串类型
        experience_data = processed_experience.get(current_round)

        if experience_data:
            # 构建 experience 字符串
            experience = f"Original Score: {experience_data['score']}\n"
            experience += "Failed modifications:\n"
            for mod in experience_data["failure"]:
                experience += f"- {mod['modification']} (Score: {mod['score']})\n"
            experience += "\n\nNote: Reference failed experiences, avoid trying failed approaches again, attempt to change your thinking, not limited to using more advanced Python syntax like for, if, else, etc., or modifying the Prompt part"
        else:
            experience = f"No experience data found for round {current_round}."

        operator_input = OPERATOR_INPUT.format(
            experinece=experience, score=score, operator=operator[0], prompt=prompt, type=self.type, graph=graph[0]
        )
        operator_system = OPERATOR_OPTIMIZE_PROMPT.format(type=self.type)

        node_prompt = operator_system + operator_input  # TODO 看一眼谁先谁后这个地方

        node = await ActionNode.from_pydantic(GraphOptimize).fill(
            context=node_prompt, mode="context_fill", llm=self.llm
        )

        max_retries = 5
        retries = 0

        while retries < max_retries:
            try:
                # TODO 需要和评测的模型分开（传入模型或其它方法），如果能实现Temperature调整更好
                response = node.instruct_content.model_dump()
                break

            except Exception as e:
                retries += 1
                print(f"Error generating prediction: {e}. Retrying... ({retries}/{max_retries})")

                if retries == max_retries:
                    print("Maximum retries reached. Skipping this sample.")
                    break
                time.sleep(5)

        # TODO 这里其实可以省去
        operator_match = response["operator"]
        prompt_match = response["prompt"]
        modification_match = response["modification"]

        modification = modification_match.group(1)
        prompt = prompt_match.group(1)
        operator = OPERATOR_TEMPLATE.format(operator=operator_match.group(1), round=self.round + 1)

        # 将 operator.py 文件写入到目录中
        with open(os.path.join(directory, "operator.py"), "w", encoding="utf-8") as file:
            file.write(operator)

        # 将 prompt.py 文件写入到目录中
        with open(os.path.join(directory, "prompt.py"), "w", encoding="utf-8") as file:
            file.write(prompt)

        # 将 prompt.py 文件写入到目录中
        with open(os.path.join(directory, "__init__.py"), "w", encoding="utf-8") as file:
            file.write("")

        experience = {
            "father node": sample["round"],
            "modification": modification,
            "before": sample["score"],
            "after": None,
            "succeed": None,
        }

        with open(os.path.join(directory, "experience.json"), "w", encoding="utf-8") as file:
            json.dump(experience, file, ensure_ascii=False, indent=4)

        score = evaluator.validation_evaluate(self.dataset, self.graph)
        experience["after"] = score
        experience["succeed"] = bool(score > experience["before"])

    def test(self, graph_path: str):
        """
        在测试集上验证最佳效果，收集Performance, Pareto Front 等指标，
        """
        pass


