SOLVE_PROMPT = """
Given the following mathematical problem, provide a step-by-step solution. Be sure to:
1. Clearly state any assumptions or given information.
2. Show all your work, including intermediate steps.
3. Use proper mathematical notation and formatting.
4. Explain your reasoning for each step.
5. Provide a final answer, clearly marked and in simplest form.

Problem:
{input}

Solve it step by step, and ensure your solution is clear and comprehensive.
"""

REVIEW_PROMPT = """
Review the following problem and its proposed solution. Your task is to:
1. Check the solution for correctness.
2. Identify any errors or missing steps.
3. Suggest improvements or alternative approaches if applicable.
4. If the solution is correct and complete, confirm its validity.
5. If improvements are needed, provide a revised solution.

{input}

Provide your review and, if necessary, an improved solution.
"""