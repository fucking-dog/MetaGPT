INITIAL_SOLUTION_PROMPT = """
You are a mathematical problem-solving expert. Your task is to solve the given mathematical problem step by step. Show your work clearly and explain each step of your reasoning. If multiple approaches are possible, choose the most efficient one. Ensure your solution is accurate and complete.

Problem: {input}

Provide your solution below:
"""

SELF_REVIEW_PROMPT = """
You are a mathematical solution reviewer. Your task is to carefully examine the given problem and its proposed solution. Check for any errors in calculations, logic, or methodology. Also, verify if the solution addresses all parts of the problem and if the steps are clearly explained.

{input}

Review the solution and provide your feedback. If you find any errors or areas for improvement, clearly state them. If the solution appears correct and complete, confirm this as well.
"""

CORRECTION_PROMPT = """
You are a mathematical problem-solving expert. Your task is to correct and improve the initial solution based on the review feedback. Address all issues mentioned in the review and ensure the final solution is accurate, complete, and clearly explained.

{input}

Provide the corrected and improved solution below:
"""