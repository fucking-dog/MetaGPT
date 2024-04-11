# -*- coding: utf-8 -*-
# Date       : 2023/4/3
# Author     : @Zhaoyang Yu @ Yufan Zhao
# email      :
# Description: The Gate Controller is the entry to the math AI. Within this class, the GateController formulates problem-solving strategies for subsequent math resolver based on the type of input question and judgments derived from human design.

from typing import Dict
import json
from math_ai.codebase.engine.llm import OpenAILLM


class GateController:
    def __init__(self):
        self.llm = OpenAILLM()
        self.role = """
            你是全球最杰出的数学竞赛选手，擅长分析数学问题并判断数学问题的类型。
            现在，你需要基于给定的数学问题，回答两个问题：1:数学问题的类型，2:判断题目是否存在小问。
            数学问题的类型仅限于：1:ALGEBRA_NUMBER_THEORY, 2:GEOMOTRY_TOPOLOGY, 3:ANALYSYS_EQUATION, 4:COMBINATION_PROBABILITY, 5:COMPUTATION
            判断题目是否存在小问，若不存在小问返回simple，存在小问则返回muti。
            请你以JSON格式进行返回，一个可以参考的格式如下,type表示数学问题的类型，if_complex表示问题是否存在小问：
            {{
                "type": <TYPE OF THE MATH PROBLEM>,
                "if_muti": <WHETHER A PROBLEM CONTAINS SEVERAL SUB-PROBLEM>
            }}
            你面临的问题是：\n
        """
        self.llm.set_role(self.role)

    def run(self, problem: Dict) -> Dict:
        """
        problem: 
        {
            "desc":"<QUESTION DESC>",
            "type":"<select from human design>",
        }

        Gate Controller choose human design strategy here
        and return strategy in dict
        you can add anything else such as problem's possible attention in dict.
        for example:
        
        return 
        {
            "strategy": "策略名称",
            "attention": "<"Attention points identified during the determination of problem types.">"
        }
        """
        prob = problem['desc']
        response = self.llm.llm_response(prob, json_mode=True)
        problem['if_muti'] = 'simple' if 'simple' in response['if_muti'] else 'muti'
        problem['strategy'] = response['type']
        return problem
    

# for test
if __name__ == "__main__":
    mygate = GateController()
    prob = """对实数$r$，用$\\Vert{r}$表示$r$和最近的整数的距离：$\\Vert{r} = \min {\\vert{r-n}:n\\in\\mathbb{Z}}$.
    试问是否存在非零实数$s$，满足$\\lim_{n\\to\\infty}\\Vert{(\\sqrt{2}+1)^ns}=0$?
    """
    print(mygate.run({'desc': prob, 'type': ''}))
