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

REVIEW_PROMPT = """
Review the integrated solution to the math problem. Check for any errors or areas that need improvement. If you find any issues, provide a corrected and improved solution. If the integrated solution is correct, confirm its accuracy and completeness.
"""

DIMENSIONAL_ANALYSIS_PROMPT = """
Examine the reviewed solution and determine if the problem involves physical quantities or measurements that require dimensional analysis or unit conversion. If applicable, perform the necessary dimensional analysis or unit conversion, ensuring that all quantities are expressed in consistent units. Update the solution to include this analysis, clearly showing how units are handled throughout the problem-solving process. If dimensional analysis is not applicable, return the solution as is.
"""

NUMERICAL_CHECK_PROMPT = """
Examine the solution after dimensional analysis and determine if it contains a clear numerical answer. If a numerical answer is present, return the solution as is. If not, attempt to derive a numerical answer from the given solution and add it to the end of the solution. Ensure the final output includes both the detailed solution and a clear numerical answer if applicable to the problem.
"""

SELF_REFLECTION_PROMPT = """
Carefully review the solution after the numerical check. Ensure that all aspects of the original problem have been addressed and that the solution is logically consistent. If any part of the problem has been overlooked or if there are any logical inconsistencies, revise the solution accordingly. Provide a final, comprehensive solution that fully answers the original problem and is logically sound.
"""