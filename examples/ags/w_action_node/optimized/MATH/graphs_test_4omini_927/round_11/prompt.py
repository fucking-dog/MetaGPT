SOLVE_PROMPT = """
You are a mathematics expert. Your task is to solve the given mathematical problem step by step. Show your work clearly and provide a final answer.

Problem:
{input}

Please follow these steps:
1. Analyze the problem and identify the key information.
2. Determine the appropriate mathematical concepts or formulas to use.
3. Solve the problem step by step, explaining each step clearly.
4. Provide a final answer, clearly marked and formatted.

Ensure your solution is clear, concise, and mathematically accurate.
"""

REVIEW_PROMPT = """
As a mathematics expert, your task is to review and improve the given solution to the mathematical problem. Please follow these steps:

1. Carefully read the problem and the provided solution.
2. Check for any errors in calculations, logic, or methodology.
3. Verify that all steps are clearly explained and justified.
4. Ensure that the final answer is correct and properly formatted.
5. If any improvements are needed, make them while maintaining the original structure of the solution.
6. If the solution is already correct and complete, simply state that no changes are needed.

Problem and Solution:
{input}

Please provide your reviewed and improved solution below:
"""