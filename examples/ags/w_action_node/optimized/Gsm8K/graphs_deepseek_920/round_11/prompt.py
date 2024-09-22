DECOMPOSE_PROMPT = """
Analyze the given math problem and break it down into smaller, manageable sub-problems. List each sub-problem on a new line. Ensure that solving all sub-problems in order will lead to the solution of the main problem.

Problem to decompose:
"""

SOLVE_PROMPT = """
Solve the given math problem step by step. Show your work clearly and provide a final answer.
After solving, extract the numerical answer and present it as follows:
Final Answer: [numerical value]

Solve it now:
"""

REVIEW_PROMPT = """
Review the problem, initial solution, and verification. Identify any errors or discrepancies. If necessary, recalculate the answer. Provide a final, corrected solution with clear reasoning.

Problem:
{problem}

Initial Solution:
{initial_solution}

Verification:
{verification}

Please review and provide the corrected solution:
"""