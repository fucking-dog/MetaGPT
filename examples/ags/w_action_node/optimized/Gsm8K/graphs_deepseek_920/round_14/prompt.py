BREAKDOWN_PROMPT = """
Analyze the given math problem and break it down into key components. Identify and list:
1. Important numerical values
2. Relationships between values
3. Steps required to solve the problem

Provide a clear, concise breakdown:
"""

SOLVE_PROMPT = """
Using the problem breakdown provided, solve the given math problem step by step. Show your work clearly and provide a final answer.
After solving, extract the numerical answer and present it as follows:
Final Answer: [numerical value]

Solve it now:
"""

REVIEW_PROMPT = """
Review the problem, initial breakdown, solution, and verification. Identify any errors or discrepancies. If necessary, recalculate the answer. Provide a final, corrected solution with clear reasoning.

Problem:
{problem}

Problem Breakdown:
{breakdown}

Initial Solution:
{initial_solution}

Verification:
{verification}

Please review and provide the corrected solution:
"""