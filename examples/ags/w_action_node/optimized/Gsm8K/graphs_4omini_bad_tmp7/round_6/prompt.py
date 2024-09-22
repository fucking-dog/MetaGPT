INITIAL_SOLVE_PROMPT = """
You are a math expert. Solve the given problem step by step, showing all your work. After solving, provide the final numerical answer without any units or explanations.

Problem:
"""

REVIEW_PROMPT = """
You are a math expert tasked with reviewing and potentially correcting a solution to a math problem. Carefully examine the problem and the initial solution. If the initial solution is correct, confirm it. If there are any errors, provide a corrected solution with a step-by-step explanation. In both cases, end your response with the final numerical answer without any units or additional text.

"""