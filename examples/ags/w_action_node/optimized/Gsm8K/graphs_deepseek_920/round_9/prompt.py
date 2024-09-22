ANALYZE_PROMPT = """
Analyze the given math problem and break it down into simpler sub-problems or steps. Identify the key information and operations needed to solve the problem.

Problem:
"""

SOLVE_PROMPT = """
Solve the given math problem step by step, considering the provided problem analysis. Show your work clearly and provide a final answer.
After solving, extract the numerical answer and present it as follows:
Final Answer: [numerical value]

Problem and Analysis:
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