MATH_SOLUTION_PROMPT = """
You are an expert mathematician. Your task is to solve the given math problem step by step. Show your work clearly and explain each step of your reasoning. If the problem involves calculations, perform them accurately. If it requires proving a statement, provide a clear and logical proof. Make sure your solution is complete and addresses all parts of the problem.

Problem: {problem}

Please provide a detailed solution:
"""

REPHRASE_PROMPT = """
As an expert in mathematics, your task is to rephrase the given math problem. The rephrased version should maintain the original meaning and all essential information, but present it in a different way that might offer new insights or perspectives on the problem. This rephrasing should aim to clarify the problem and potentially make it easier to approach or solve.

Original problem:
{input}

Please provide a rephrased version of this problem:
"""