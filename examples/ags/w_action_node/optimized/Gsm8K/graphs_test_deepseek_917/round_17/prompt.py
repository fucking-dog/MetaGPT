SOLVE_PROMPT1 = """
Solve the given math problem step by step, focusing on algebraic methods. Show your work and explain each step clearly.
"""

SOLVE_PROMPT2 = """
Solve the given math problem step by step, using geometric or visual approaches when applicable. Show your work and explain each step clearly.
"""

SOLVE_PROMPT3 = """
Solve the given math problem step by step, emphasizing logical reasoning and problem-solving strategies. Show your work and explain each step clearly.
"""

FORMULA_CHECK_PROMPT = """
Analyze the given problem and the three solution approaches. Identify any relevant mathematical formulas or equations that could be applied to simplify or solve the problem more efficiently. If applicable, explain how these formulas could be used in the context of the problem and how they might improve the solution process.
"""

INTEGRATE_PROMPT = """
Compare the three given solutions and the formula check for the math problem. Identify the strengths of each approach and create an integrated solution that combines the best aspects of all three, incorporating any relevant formulas or equations identified. Ensure the final solution is clear, comprehensive, and mathematically sound.
"""

REVIEW_PROMPT = """
Review the integrated solution to the math problem. Check for any errors or areas that need improvement. If you find any issues, provide a corrected and improved solution. If the integrated solution is correct, confirm its accuracy and completeness.
"""

NUMERICAL_CHECK_PROMPT = """
Examine the reviewed solution and determine if it contains a clear numerical answer. If a numerical answer is present, return the solution as is. If not, attempt to derive a numerical answer from the given solution and add it to the end of the solution. Ensure the final output includes both the detailed solution and a clear numerical answer if applicable to the problem.
"""

SELF_REFLECTION_PROMPT = """
Carefully review the solution after the numerical check. Ensure that all aspects of the original problem have been addressed and that the solution is logically consistent. If any part of the problem has been overlooked or if there are any logical inconsistencies, revise the solution accordingly. Provide a final, comprehensive solution that fully answers the original problem and is logically sound.
"""