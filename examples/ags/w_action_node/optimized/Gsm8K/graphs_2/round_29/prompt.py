THINK_PROMPT = """
Please reason step by step, think about what you know and what you need to solve.
"""

REVIEW_PROMPT = """
Please review the following solution to the given problem. Ensure it is correct, complete, and addresses all aspects of the problem. If there are any issues, provide specific feedback for improvement.

Problem: {problem}
Solution: {solution}

Is the solution correct and complete? (Yes/No)
Feedback (if any):
"""

REVISE_PROMPT = """
Please revise the following solution based on the given feedback. Ensure that the revised solution addresses all the issues mentioned in the feedback and solves the problem correctly.

Problem: {problem}
Original Solution: {solution}
Feedback: {feedback}

Revised Solution:
"""