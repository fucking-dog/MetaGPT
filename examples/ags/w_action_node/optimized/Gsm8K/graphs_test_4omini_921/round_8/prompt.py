ANALYZE_PROMPT = """
Analyze the given math problem. Identify the key information, variables, and operations needed to solve it. Provide a step-by-step approach to solving the problem, but do not perform any calculations.

Problem:
{input}

Provide your analysis:
"""

SOLVE_PROMPT1 = """
Solve the given math problem using the provided analysis and code output. Focus on a direct, straightforward approach. Ensure your solution is clear, concise, and provides the final answer in a format that can be easily extracted (e.g., "Final answer: X").

Problem:
{input}

Provide your solution:
"""

SOLVE_PROMPT2 = """
Solve the given math problem using the provided analysis and code output. Use a step-by-step approach, showing all your work. Ensure your solution is clear, concise, and provides the final answer in a format that can be easily extracted (e.g., "Final answer: X").

Problem:
{input}

Provide your solution:
"""

SOLVE_PROMPT3 = """
Solve the given math problem using the provided analysis and code output. Approach the problem from a different angle or use an alternative method if possible. Ensure your solution is clear, concise, and provides the final answer in a format that can be easily extracted (e.g., "Final answer: X").

Problem:
{input}

Provide your solution:
"""