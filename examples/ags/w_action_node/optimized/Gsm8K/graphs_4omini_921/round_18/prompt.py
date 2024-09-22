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
Solve the given math problem using the provided analysis and code output. Focus on breaking down the problem into smaller steps and solving each step separately. Ensure your solution is clear, concise, and provides the final answer in a format that can be easily extracted (e.g., "Final answer: X").

Problem:
{input}

Provide your solution:
"""

SOLVE_PROMPT3 = """
Solve the given math problem using the provided analysis and code output. Focus on using alternative methods or approaches if possible. Ensure your solution is clear, concise, and provides the final answer in a format that can be easily extracted (e.g., "Final answer: X").

Problem:
{input}

Provide your solution:
"""

DOUBLE_CHECK_PROMPT = """
Double-check the initial solution for the given math problem using a different approach. If possible, use a different method or perspective to verify the answer. Provide a step-by-step explanation of your verification process and the result.

Problem:
{input}

Provide your double-check solution:
"""

NUMERICAL_CHECK_PROMPT = """
Perform a numerical extraction and validation on the initial solution and double-check solution. Extract all numerical values from both solutions, including intermediate calculations and final answers. Compare these values and identify any discrepancies. If there are discrepancies, determine which value is more likely to be correct based on the problem context and mathematical reasoning. Provide a summary of your findings and a recommended numerical answer.

Problem:
{input}

Provide your numerical check:
"""

FINAL_SOLUTION_PROMPT = """
Compare the initial solution, double-check solution, and numerical check. Determine the final answer based on this comparison. If there are discrepancies, explain why you chose one answer over the others. Consider the numerical validation in your decision-making process. Provide the final answer in a clear, extractable format (e.g., "Final answer: X").

Problem:
{input}

Provide your final solution:
"""