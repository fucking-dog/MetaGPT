# -*- coding: utf-8 -*-
# @Date    : 1/11/2025 17:26 PM
# @Author  : didi
# @Desc    : optimizer demo of eflow

from metagpt.llm import LLM
from metagpt.ext.eflow.src.abstract import Workflow
from metagpt.configs.models_config import ModelsConfig
from metagpt.provider.llm_provider_registry import create_llm_instance
from metagpt.utils.cost_manager import CostManager
from metagpt.ext.eflow.src.optimize_operators import AttributeQueryOperator, AttributeOverallOperator, WorkflowOptimizeOperator
from metagpt.logs import logger
from typing import List
import json
import asyncio



class OptimizeNode:
    def __init__(self, depth:int, layer_id:int, save_path):
        self.depth = depth
        self.layer_id = layer_id
        self.save_path = save_path
        self.workflow = None
        self.prompt = None
        self.case_table = None

        self.father_node = None
        self.child_nodes = []

        self.analysis_table = None
        self.attribute_table = None
        self.optimize_signal_compared_with_father = None

    def __str__(self):
        return f"OptimizeNode(node_id={self.node_id}, workflow={self.workflow}, prompt={self.prompt}, case_table={self.case_table}, father_node={self.father_node})"
    
    def _save(self):
        pass

    def _load(self):
        pass

    def _combine_optimize_signals(self):
        optimize_signals = "对当前Workflow的改进信号:\n" + self.optimize_signal_compared_with_father + "\n"
        for child_node in self.child_nodes:
            optimize_signals += child_node.optimize_signal_compared_with_father
        return optimize_signals

class Optimizer:
    def __init__(self, dataset, optimize_model, operator_description:str, max_round:int =10):
        self.dataset = dataset
        self.optimize_model = optimize_model
        self.workflow_optimize_operator = WorkflowOptimizeOperator(self.optimize_model)
        self.operator_description = operator_description # TODO 这里我写死了，之后你用Graph utils 应该就有，我看你之前有写
        self.max_round = max_round

    def optimize_on_model_choice(self, workflow: Workflow, model_choices: List):
        """
        optimize the model choice of workflow's different nodes
        It's a multi-objective optimization problem.
        """
        pass

    def optimize_on_workflow_structure(self, workflow, prompts, optimize_signal):
        """
        optimize the workflow's structure.
        optimize signal is from the attributor.

        The attributor design should be dynamic on different datasets.

        when conducting optimization, the optimizer should see
        1. analysis_table
        2. attribute_table
        3. optimize_signal
        """
        response = self.workflow_optimize_operator(
            optimize_signal=optimize_signal, 
            raw_workflow=workflow, 
            custom_prompt=prompts, 
            operator_description=self.operator_description
        )
        modification = response["modification"]
        optimize_workflow = response["workflow"]
        optimize_prompts = response["prompt"]
        
        logger.info(json.dumps(modification, indent=4))
        logger.info(json.dumps(optimize_workflow, indent=4))
        logger.info(json.dumps(optimize_prompts, indent=4))
        
        return response

    def optimize(self):
        """
        full process of workflow optimization. 
        """
        for _ in range(self.max_round):
        
        pass




class Attributor:
    def __init__(self, dataset, attribute_query_model_name, attribute_overall_model_name, score_threshold=0.5):
        self.dataset = dataset
        self.score_threshold = score_threshold

        attribute_query_llm_config = ModelsConfig.default().get(attribute_query_model_name)
        self.attribute_query_model = create_llm_instance(attribute_query_llm_config)
        self.attribute_query_model.cost_manager = CostManager()

        attribute_overall_llm_config = ModelsConfig.default().get(attribute_overall_model_name)
        self.attribute_overall_model = create_llm_instance(attribute_overall_llm_config)
        self.attribute_overall_model.cost_manager = CostManager()

        self.attribute_query_operate = AttributeQueryOperator(self.attribute_query_model)
        self.attribute_overall_operate = AttributeOverallOperator(self.attribute_overall_model)
        self.current_raw_case_table = None
        self.current_optimized_case_table = None
        

    def craft_analysis_table(self):
        analysis_table = {
            'raw_better': [],   
            'opt_better': [],   
            'both_low': [],    
        }
        
        for question_id in self.current_raw_case_table['cases']:
            raw_score = float(self.current_raw_case_table['cases'][question_id]['score'])
            opt_score = float(self.current_optimized_case_table['cases'][question_id]['score'])

            if raw_score > opt_score:
                analysis_table['raw_better'].append(question_id)
            elif raw_score < opt_score:
                analysis_table['opt_better'].append(question_id)
            elif raw_score < self.score_threshold and opt_score < self.score_threshold:
                analysis_table['both_low'].append(question_id)
        
        return analysis_table

    async def attribute_on_analysis_table(self, analysis_table, max_concurrent=10):
        attribute_table = {
            "raw_better": [],
            "opt_better": [],
            "both_low": []
        }
        
        # 创建信号量来控制并发数量
        semaphore = asyncio.Semaphore(max_concurrent)
        
        # 创建一个包装函数来使用信号量
        async def run_with_semaphore(key, task):
            async with semaphore:
                result = await task
                return key, result
        
        # 创建所有任务的列表
        tasks = []
        for key in analysis_table:
            if len(analysis_table[key]) > 0:
                for question_id in analysis_table[key]:
                    task = self.attribute_query_operate(
                        raw_workflow=self.current_raw_case_table['workflow'],
                        opt_workflow=self.current_optimized_case_table['workflow'],
                        question_description=self.current_raw_case_table['cases'][question_id]['question'],
                        raw_answer=self.current_raw_case_table['cases'][question_id]['answer'],
                        opt_answer=self.current_optimized_case_table['cases'][question_id]['answer'],
                        mode=key
                    )
                    tasks.append(run_with_semaphore(key, task))
        
        # 并发执行所有任务
        results = await asyncio.gather(*tasks)
        
        # 将结果放入对应的类别中
        for key, result in results:
            attribute_table[key].append(result["attribution_on_workflow"])

        return attribute_table
    
    async def attribute_on_attribute_table(self, attribute_table):
        """
        形成优化信号
        """
        attribute_conclusion = await self.attribute_overall_operate(
            workflow=self.current_optimized_case_table['workflow'],
            attribution_list=attribute_table
        )
        return attribute_conclusion
    
    async def attribute(self, raw_case_table, optimized_case_table):
        """
        attribute on the wrong case
        """
        self.current_raw_case_table = raw_case_table
        self.current_optimized_case_table = optimized_case_table
        
        analysis_table = self.craft_analysis_table()
        logger.info("analysis_table:")
        logger.info(json.dumps(analysis_table, indent=4))

        attribute_table = await self.attribute_on_analysis_table(analysis_table, max_concurrent=20)
        logger.info("attribute_table:")
        logger.info(json.dumps(attribute_table, indent=4))

        optimize_signal = await self.attribute_on_attribute_table(attribute_table)
        logger.info("optimize_signal:")
        logger.info(json.dumps(optimize_signal, indent=4))

        return optimize_signal, self.attribute_query_model.cost_manager.total_cost, self.attribute_overall_model.cost_manager.total_cost
    

# TODO 使用HumanEval 进行测试（小样本错误量）
# TODO 使用MBPP 进行测试（大样本错误量，大样本错误量任务似乎应该进行Sample
# TODO 现在看起来，只是输入workflow数据，不输入reason process 数据，似乎也是可行的，只是无法保证效果


# TODO 归因过程中，需要区分清Answer与Workflow的差异，似乎可以用一个
# TODO Sample 机制
# TODO Conclusion -> Optimize 机制
# TODO CodeContests Benchmark @fashen
# TODO output 出错这里应该有一个retry机制，不应该直接错了
# TODO 现在的优化机制，只有利用经验，而没有探索，并且没有结合Operator的内容
# TODO Operator的内容也应该被丢进归因过程之中。


# Case Table Structure
{
    "workflow":"include workflow code, and corresponding prompts",
    "cases":{
        "question_id":{
            "question":"",
            "answer":"",
            "score":""
        }
    }
}