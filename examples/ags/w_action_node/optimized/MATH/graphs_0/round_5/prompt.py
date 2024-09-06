THINK_PROMPT = """
Please reason step by step, think about what you know and what you need to solve.
"""

SELF_ASK_PROMPT = """
Based on your initial thoughts, what additional questions should you ask yourself to solve this problem more effectively? List these questions and provide brief answers to each.
"""

REVIEW_PROMPT = """
Please review the solution to the given problem. Check for correctness, completeness, and clarity.
If the solution is correct and complete, return True. If not, return False and provide feedback on what needs to be improved.
"""

REVISE_PROMPT = """
Based on the given feedback, please revise the solution to address the issues mentioned.
Ensure that the revised solution is correct, complete, and clear.
"""

SC_ENSEMBLE_PROMPT = """
Given multiple solutions to the same problem, please evaluate them for consistency and accuracy. 
Synthesize the most reliable and correct solution based on the common elements and strengths of each provided solution.
Ensure that the final solution is comprehensive, accurate, and addresses all aspects of the problem.
"""