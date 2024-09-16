MATH_SOLUTION_PROMPT = """
You are an expert mathematician. Your task is to solve the given math problem step by step. Show your work clearly and explain each step of your reasoning. If the problem involves calculations, perform them accurately. If it requires proving a statement, provide a clear and logical proof. Make sure your solution is complete and addresses all parts of the problem.

Problem: {problem}

Please provide a detailed solution:
"""

REPHRASE_PROMPT = """
As an expert in mathematics, your task is to rephrase the given math problem. The goal is to maintain the original meaning and complexity while presenting it in a different way. This rephrasing should provide additional context or perspective that might help in solving the problem. Please ensure that all essential information from the original problem is preserved in your rephrasing.

Original problem: {input}

Please provide a rephrased version of the problem:
"""