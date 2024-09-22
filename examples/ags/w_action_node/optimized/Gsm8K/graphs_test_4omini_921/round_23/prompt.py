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

ALTERNATIVE_SOLVE_PROMPT = """
Solve the given math problem using a different approach from the standard method. Consider alternative techniques or perspectives to arrive at the solution. Ensure your solution is clear, concise, and provides the final answer in a format that can be easily extracted (e.g., "Final answer: X").

Problem:
{input}

Provide your alternative solution:
"""

DOUBLE_CHECK_PROMPT = """
Double-check the initial solution for the given math problem using a different approach. If possible, use a different method or perspective to verify the answer. Provide a step-by-step explanation of your verification process and the result.

Problem:
{input}

Provide your double-check solution:
"""

FINAL_SOLUTION_PROMPT = """
Compare the initial solution and the double-check solution. Determine the final answer based on this comparison. If there's a discrepancy, explain why you chose one answer over the other. Provide the final answer in a clear, extractable format (e.g., "Final answer: X").

Problem:
{input}

Provide your final solution:
"""