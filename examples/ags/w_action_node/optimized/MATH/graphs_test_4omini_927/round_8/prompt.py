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
As a mathematics expert, your task is to review and improve the given solution to the mathematical problem. Ensure the solution is accurate, complete, and clearly explained.

{input}

Please follow these steps:
1. Check if the initial solution correctly identifies all key information from the problem.
2. Verify that the mathematical concepts and formulas used are appropriate and correctly applied.
3. Ensure that each step of the solution is logically sound and clearly explained.
4. Check if the final answer is correct and properly formatted.
5. If you find any errors or areas for improvement, provide corrections or suggestions.
6. If the solution is correct and complete, state that it is verified.

Provide your review and, if necessary, an improved solution. Ensure your response is clear, concise, and mathematically rigorous.
"""