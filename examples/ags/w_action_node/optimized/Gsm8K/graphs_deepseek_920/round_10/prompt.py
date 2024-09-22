SOLVE_PROMPT = """
Solve the given math problem step by step. Show your work clearly and provide a final answer.
After solving, extract the numerical answer and present it as follows:
Final Answer: [numerical value]

Solve it now:
"""

ERROR_CHECK_PROMPT = """
Review the given problem and solution. Check for common errors in mathematical reasoning and calculation. Focus on:
1. Misinterpretation of the problem statement
2. Incorrect mathematical operations
3. Unit conversion errors
4. Overlooking important information

If you find any errors, explain them clearly. If no errors are found, state "No errors found."

Problem and Solution:
"""

CORRECT_SOLUTION_PROMPT = """
Given the problem, original solution, and error check results, provide a corrected solution. Show your work step by step and ensure all identified errors are addressed.

After solving, extract the numerical answer and present it as follows:
Final Answer: [numerical value]

Provide the corrected solution now:
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