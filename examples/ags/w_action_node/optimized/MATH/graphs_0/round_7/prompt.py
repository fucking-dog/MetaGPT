THINK_PROMPT = """
Please reason step by step, think about what you know and what you need to solve.
"""

REVIEW_PROMPT = """
Please review the solution to the given problem. Check for correctness, completeness, and clarity.
If the solution is correct and complete, return True. If not, return False and provide feedback on what needs to be improved.
"""

REVISE_PROMPT = """
Based on the given feedback, please revise the solution to address the issues mentioned.
Ensure that the revised solution is correct, complete, and clear.
"""