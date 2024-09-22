ANALYZE_PROMPT = """
Analyze the given math problem. Identify the key information, variables, and operations needed to solve it. Provide a step-by-step approach to solving the problem, but do not perform any calculations.

Problem:
{input}

Provide your analysis:
"""

SOLVE_PROMPT = """
Solve the given math problem using the provided analysis and code output. Ensure your solution is clear, concise, and provides the final answer in a format that can be easily extracted (e.g., "Final answer: X").

Problem:
{input}

Provide your solution:
"""

SOLVE_PROMPT_ALT = """
Solve the given math problem using an alternative approach. Consider using a different method or perspective than the one used in the initial analysis. Provide a step-by-step solution and clearly state the final answer.

Problem:
{input}

Provide your alternative solution:
"""

SOLVE_PROMPT_NUMERIC = """
Solve the given math problem focusing on numerical calculations. Break down the problem into smaller steps, perform each calculation explicitly, and show your work. Provide the final answer in a clear, numerical format.

Problem:
{input}

Provide your numeric solution:
"""

DOUBLE_CHECK_PROMPT = """
Double-check the best solution for the given math problem. Verify the calculations, logic, and approach used. If you find any errors or discrepancies, provide a corrected solution. Otherwise, confirm the validity of the best solution.

Problem:
{input}

Provide your double-check solution:
"""

FINAL_SOLUTION_PROMPT = """
Compare the best solution and the double-check solution. Determine the final answer based on this comparison. If there's a discrepancy, explain why you chose one answer over the other. Provide the final answer in a clear, extractable format (e.g., "Final answer: X").

Problem:
{input}

Provide your final solution:
"""