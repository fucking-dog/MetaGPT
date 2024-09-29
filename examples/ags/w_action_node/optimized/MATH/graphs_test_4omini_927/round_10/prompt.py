SOLVE_PROMPT = """
You are a math expert tasked with solving complex mathematical problems. Please provide a step-by-step solution to the given problem, showing all your work and reasoning. Be sure to:

1. Clearly state any assumptions or given information.
2. Break down the problem into smaller, manageable steps.
3. Use appropriate mathematical notation and formulas.
4. Explain each step of your reasoning.
5. Double-check your calculations and logic.
6. Provide a clear, concise final answer.

Remember to format your answer in a way that's easy to read and understand. Use LaTeX notation for mathematical expressions when appropriate.

Problem:
{input}

Solution:
"""

REVIEW_PROMPT = """
As a mathematical expert, your task is to review and potentially improve the proposed solution to the given problem. Please follow these steps:

1. Carefully read the problem statement and the proposed solution.
2. Check for any errors in logic, calculations, or reasoning.
3. Verify that all steps are clearly explained and justified.
4. Ensure that the final answer is correct and properly stated.
5. If you find any issues, provide corrections and explanations.
6. If the solution is correct but could be improved, suggest enhancements for clarity or efficiency.
7. If the solution is already optimal, confirm its correctness and completeness.

Please provide your review and, if necessary, an improved solution. Use LaTeX notation for mathematical expressions when appropriate.

Problem and Proposed Solution:
{input}

Review and Improved Solution (if needed):
"""