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
Compare the three given solutions for the math problem. Identify the strengths of each approach and create an integrated solution that combines the best aspects of all three. Ensure the final solution is clear, comprehensive, and mathematically sound.
"""

THEOREM_CHECK_PROMPT = """
Examine the integrated solution and identify any mathematical properties or theorems that could be applied to simplify or enhance the solution. If applicable, apply these properties or theorems to refine the solution, making it more elegant or efficient. Explain the reasoning behind using these mathematical concepts and how they improve the solution.
"""

REVIEW_PROMPT = """
Review the solution after the theorem check. Verify the correct application of any mathematical properties or theorems. Check for any errors or areas that need improvement. If you find any issues, provide a corrected and improved solution. If the solution is correct, confirm its accuracy, completeness, and efficiency.
"""

NUMERICAL_CHECK_PROMPT = """
Examine the reviewed solution and determine if it contains a clear numerical answer. If a numerical answer is present, return the solution as is. If not, attempt to derive a numerical answer from the given solution and add it to the end of the solution. Ensure the final output includes both the detailed solution and a clear numerical answer if applicable to the problem.
"""

SELF_REFLECTION_PROMPT = """
Carefully review the solution after the numerical check. Ensure that all aspects of the original problem have been addressed, the solution is logically consistent, and any applied mathematical properties or theorems are correctly used. If any part of the problem has been overlooked or if there are any logical inconsistencies, revise the solution accordingly. Provide a final, comprehensive solution that fully answers the original problem, is logically sound, and demonstrates an advanced understanding of mathematical concepts.
"""