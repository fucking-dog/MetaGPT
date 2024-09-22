TIME_CALC_PROMPT = """
If the problem involves a time duration, calculate the total number of hours. If not, respond with 'N/A'.

For example:
- "from 8:00 AM until 11:00 PM" would be 15 hours.
- "from 9:30 AM to 2:45 PM" would be 5.25 hours.

Provide only the numerical answer or 'N/A'. Do not include any explanations.

Calculate now:
"""

SOLVE_PROMPT = """
Solve the given math problem step by step. Show your work clearly and provide a final answer.
Pay special attention to any time-based calculations, using the provided working hours if applicable.
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