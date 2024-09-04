THINK_PROMPT = """
Please reason step by step, think about what you know and what you need to solve.
"""

SELF_ASK_PROMPT = """
Based on the problem and initial thoughts, ask yourself relevant questions that would help in solving the problem. Then, provide answers to these questions.
"""

GENERATE_PROMPT = """
Generate a solution to the problem using a {approach} approach. Provide a step-by-step explanation of your solution.
"""

REVIEW_PROMPT = """
Please review the solution to the given problem. Check for correctness, completeness, and clarity.
If the solution is correct and complete, return True. If not, return False and provide feedback on what needs to be improved.
"""

REVISE_PROMPT = """
Based on the given feedback, please revise the solution to address the issues mentioned.
Ensure that the revised solution is correct, complete, and clear.
"""

FU_ENSEMBLE_PROMPT = """
Critically evaluate the given solutions for the problem. Synthesize an enhanced integrated solution that combines the strengths of each approach while addressing any weaknesses or inconsistencies.
Ensure the final solution is correct, complete, and clear.
"""