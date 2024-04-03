# -*- coding: utf-8 -*-
# Date       : 2023/4/3
# Author     : @Zhaoyang Yu @ Yufan Zhao
# email      :
# Description: The Gate Controller is the entry to the math AI. Within this class, the GateController formulates problem-solving strategies for subsequent math resolver based on the type of input question and judgments derived from human design.

from typing import Dict
from math_ai.codebase.llm.llm import OpenAILLM


class GateController:
    def __init__(self):
        self.llm = OpenAILLM()
        self.role = "<TODO Here is Gate Controller's system prompt>"
        self.llm.set_role(self.role)
    def run(self, problem: Dict) -> Dict:
        """
        Gate Controller choose human design strategy here
        and return strategy in dict
        you can add anything else such as problem's possible attention in dict.
        for example:
        {
            "strategy": "<content>",
            "attention": "<"Attention points identified during the determination of problem types.">"
        }
        """

        return {"strategy":"<content>"}


