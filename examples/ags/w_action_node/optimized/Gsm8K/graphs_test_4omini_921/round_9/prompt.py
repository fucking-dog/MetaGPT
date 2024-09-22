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

VERIFY_PROMPT = """
Carefully review the initial solution to the given math problem. Verify the calculations, logic, and final answer. If you find any errors, provide a corrected solution. If the initial solution is correct, confirm it. Always state the final answer clearly as "Final answer: X" at the end of your response.

Problem:
{input}

Verify the solution and provide the final answer:
"""