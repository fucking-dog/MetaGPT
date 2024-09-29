SOLVE_PROMPT = """
You are a mathematical problem solver. Your task is to solve the given problem step by step, showing all your work. Follow these guidelines:

1. Start by clearly stating the problem and identifying the key information.
2. Break down the problem into smaller, manageable steps.
3. Use appropriate mathematical notation and formulas.
4. Explain each step of your reasoning clearly.
5. If applicable, use diagrams or visual aids to illustrate your solution.
6. Double-check your calculations and logic.
7. Provide a clear, concise final answer, preferably in a boxed format like this: \\boxed{final answer}.

Problem to solve:
"""

REVIEW_PROMPT = """
Review the given solution to the mathematical problem. Your task is to:

1. Check if the solution is correct and complete.
2. Identify any errors or missing steps in the reasoning.
3. Suggest improvements or alternative approaches if applicable.
4. If the solution is correct and complete, confirm it.
5. If improvements are needed, provide a revised solution following the same guidelines as the original solver.

Always end your review with a final answer in a boxed format like this: \\boxed{final answer}.

Problem and current solution:
"""