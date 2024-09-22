SOLVE_PROMPT = """
Solve the given math problem step by step. Show your work clearly and provide a final answer.
Pay special attention to time calculations and percentage increases.
After solving, extract the numerical answer and present it as follows:
Final Answer: [numerical value]

Solve it now:
"""

REVIEW_PROMPT = """
Review the problem, initial solution, and double-check results. Identify any errors or discrepancies. If necessary, recalculate the answer. Provide a final, corrected solution with clear reasoning.

Problem:
{problem}

Initial Solution:
{initial_solution}

Double-check:
{double_check}

Please review and provide the corrected solution:
"""