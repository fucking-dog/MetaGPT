ANALYZE_PROMPT = """
Analyze the given math problem. Determine if it requires a numerical answer or a more conceptual/theoretical response. Identify key components of the problem, including given information, unknowns, and any specific mathematical concepts or formulas that may be relevant.
"""

SOLVE_PROMPT1 = """
Solve the given math problem step by step, focusing on algebraic methods. Show your work and explain each step clearly.
"""

SOLVE_PROMPT2 = """
Solve the given math problem step by step, using geometric or visual approaches when applicable. Show your work and explain each step clearly.
"""

SOLVE_PROMPT3 = """
Solve the given math problem step by step, emphasizing logical reasoning and problem-solving strategies. Show your work and explain each step clearly.
"""

INTEGRATE_PROMPT = """
Compare the three given solutions and the problem analysis for the math problem. Identify the strengths of each approach and create an integrated solution that combines the best aspects of all three, taking into account the initial problem analysis. Ensure the final solution is clear, comprehensive, and mathematically sound.
"""

REVIEW_PROMPT = """
Review the integrated solution to the math problem. Check for any errors or areas that need improvement. If you find any issues, provide a corrected and improved solution. If the integrated solution is correct, confirm its accuracy and completeness.
"""

NUMERICAL_CHECK_PROMPT = """
Based on the problem analysis and the reviewed solution, determine if a numerical answer is required. If a numerical answer is needed and present, verify its correctness. If a numerical answer is needed but not provided, derive it from the solution. If the problem doesn't require a numerical answer, ensure the solution adequately addresses the conceptual aspects of the problem. Adjust the solution as necessary to fully address the problem's requirements.
"""

SELF_REFLECTION_PROMPT = """
Carefully review the solution after the numerical check. Ensure that all aspects of the original problem have been addressed and that the solution is logically consistent. If any part of the problem has been overlooked or if there are any logical inconsistencies, revise the solution accordingly. Provide a final, comprehensive solution that fully answers the original problem and is logically sound.
"""