import base64
from typing import Any, Callable, List, Tuple
from pathlib import Path

import re
from metagpt.provider.llm_provider_registry import create_llm_instance
from metagpt.ext.aflow.benchmark.benchmark import BaseBenchmark
from metagpt.logs import logger
from metagpt.ext.eflow.src.abstract import Operator
from metagpt.llm import LLM

class VisualizationCompare(Operator):
    def __init__(self, model:LLM):
        super().__init__(model, "VisualizationCompare")
        self.schema = [
            {"name": "thought", "type": "str", "description": "The thought process of score"},
            {"name": "score", "type": "str", "description": "The score of the generated plot, from 0-100"}
        ]

    async def __call__(self, query:str, images: List[str]):
        prompt = """
You are an excellent judge at evaluating visualization plots between a model-generated plot and the ground truth.
You will be giving scores on how well it matches the ground truth plot.
The generated plot will be given to you as the first figure. If the first figure is blank, that means the code failed to generate a figure.
Another plot will be given to you as the second figure, which is the desired outcome of the user query, meaning it is the ground truth for you to reference.
Please compare the two figures head to head and rate them. Suppose the second figure has a score of 100, rate the first figure on a scale from 0 to 100.
Scoring should be carried out regarding the plot correctness: Compare closely between the generated plot and the ground truth, the more resemblance the generated plot has compared to the ground truth, the higher the score. 
The score should be proportionate to the resemblance between the two plots.
In some rare occurrences, see if the data points are generated randomly according to the query, if so, the generated plot may not perfectly match the ground truth, but it is correct nonetheless.
Only rate the first figure, the second figure is only for reference.
If the first figure is blank, that means the code failed to generate a figure. Give a score of 0 on the Plot correctness.
After scoring from the above aspect, please give a final score. 
The user query is {query}
        """
        prompt = prompt.format(query=query)
        response = await self._fill_node(op_schema=self.schema, prompt=prompt, format="xml_fill", images=images)
        return response["score"]


class MatPlotBench(BaseBenchmark):
    def __init__(self, name: str, file_path: str, log_path: str, llm_config):
        super().__init__(name, file_path, log_path)
        self.eval_llm = create_llm_instance(llm_config)

    def encode_image(self, image_path: str) -> str:
        """将图片编码为base64字符串"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    async def evaluate_problem(self, data: dict, graph: Callable) -> Tuple[str, str, str, float, float]:
        """评估单个可视化问题
        
        Args:
            data: 包含测试数据的字典
            graph: 生成图表的函数
        
        Returns:
            Tuple[输入文本, 生成的图片路径, 期望的图片路径, 分数, 成本]
        """
        query = data["simple_instruction"]
        test_id = data["test_id"]
        
        try:
            # 生成图表
            generated_image, cost = await graph(query)
            ground_truth = f"./benchmark_data/ground_truth/example_{test_id}.png"

            # 如果生成的图片不存在，返回0分
            if not Path(generated_image).exists():
                logger.warning(f"Generated image does not exist: {generated_image}")
                return query, generated_image, ground_truth, 0.0, cost

            # 评估图表质量
            score = await self._evaluate_plot(ground_truth, generated_image)
            
            return query, generated_image, ground_truth, score, cost

        except Exception as e:
            logger.error(f"Error evaluating plot: {e}")
            return query, "", ground_truth, 0.0, 0.0

    async def _evaluate_plot(self, ground_truth: str, generated_image: str) -> float:
        """使用GPT-4V评估图表质量"""
        visual_compare = VisualizationCompare(self.eval_llm)
        score = await visual_compare([generated_image, ground_truth])
        return score

    def calculate_score(self, expected_output: Any, prediction: Any) -> Tuple[float, Any]:
        """分数计算已在evaluate_problem中完成，这里仅返回占位值"""
        return 0.0, prediction

    def get_result_columns(self) -> List[str]:
        """定义结果CSV的列名"""
        return ["query", "generated_image", "ground_truth", "score", "cost"]
