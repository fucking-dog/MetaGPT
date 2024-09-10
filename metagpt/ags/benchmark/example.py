#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/9/13 12:29
@Author  : femto Zheng
@File    : utils from https://github.com/femto/minion
"""
import asyncio

from metagpt.llm import LLM
from metagpt.ags.w_action_node.operator import Generate
from metagpt.provider.llm_provider_registry import create_llm_instance

# 初始化LLM模型，这里使用的最基础的从config llm中加载，如果需要使用多个llm，可以去看下ModelConfig部分
# llm = LLM()

from metagpt.configs.models_config import ModelsConfig

# 配置实验参数
dataset = "Gsm8K"  # 数据集选择为GSM8K
sample = 6  # 采样数量
q_type = "math"  # 问题类型为数学
optimized_path = "examples/ags/w_action_node/optimized"  # 优化结果保存路径

# 初始化LLM模型
deepseek_llm_config = ModelsConfig.default().get("deepseek-coder")
claude_llm_config = ModelsConfig.default().get("claude-3-5-sonnet-20240620")


llm1=create_llm_instance(deepseek_llm_config)
llm2=create_llm_instance(claude_llm_config)
llm3=create_llm_instance(ModelsConfig.default().get("gpt-4-0125"))

# 设置Operator的llm 调用方式，需要在operator.py中指定
# 1. 不设置 mode，默认使用 json 解析；且描述会被编译进入prompt之中
# 2. 设置 mode 为 code_fill，使用针对code设计的提取方式解析
# 3. 设置 mode 为 context_fill，使用xml 解析
# 4. 所有的解析方式返回都是一个Dict，与你使用的action_node 的字段一致

# 修改operator对应的prompt，需要在prompt.py中修改
# 修改operator对应的action node，需要在operator_an.py中修改

generate = Generate(llm3)
async def main():
    result = await generate(problem_description="1+1=?")
    print(result)

asyncio.run(main())

# {'response': 'The solution to the problem \\(1 + 1\\) is straightforward:\n\n\\[ 1 + 1 = 2 \\]\n\nThis is a basic arithmetic operation where you add the number 1 to itself, resulting in the number 2.'}