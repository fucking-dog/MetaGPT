MATH_SOLUTION_PROMPT = """
You are an expert mathematician. Your task is to solve the given math problem step by step. Show your work clearly and explain each step of your reasoning. If the problem involves calculations, perform them accurately. If it requires proving a statement, provide a clear and logical proof. Make sure your solution is complete and addresses all parts of the problem.

Problem: {problem}

Please provide a detailed solution:
"""

REPHRASE_PROMPT = """
As an expert in mathematics, your task is to rephrase the given math problem. The rephrasing should:
1. Maintain the original meaning and all important details of the problem.
2. Use clear and concise language.
3. Potentially provide additional context or clarification that might help in solving the problem.
4. Not solve the problem, only rephrase it.

Here's the problem to rephrase:

{input}

Please provide the rephrased version of the problem:
"""