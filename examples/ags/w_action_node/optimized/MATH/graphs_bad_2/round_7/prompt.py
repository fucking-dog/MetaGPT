DETAILED_ANALYSIS_PROMPT = """
Provide a detailed analysis of the given mathematical problem. Break down the problem into its key components, identify relevant formulas or mathematical concepts, and outline a step-by-step approach to solve it. If applicable, suggest potential Python calculations that could be useful in solving the problem.

Problem:
"""

CALCULATION_VALIDATION_PROMPT = """
Review the Python calculation result for the given problem. Verify if the calculation is correct and relevant to solving the problem. If there are any errors or improvements needed, provide suggestions. If the calculation is correct and sufficient, confirm its validity.

Problem and calculation result:
"""

FINAL_SOLUTION_PROMPT = """
Using the validated calculation result and your mathematical knowledge, provide a comprehensive solution to the problem. Explain each step clearly, show all necessary work, and present the final answer in a well-formatted manner.

Problem and validated calculation result:
"""

FALLBACK_SOLUTION_PROMPT = """
Solve the given mathematical problem without relying on Python calculations. Break down the problem into steps, show all necessary work, and provide a clear, detailed solution with a final answer.

Problem:
"""

CONSISTENCY_CHECK_PROMPT = """
Review the proposed solution for the given problem. Check for logical consistency, mathematical accuracy, and completeness. Identify any potential errors or areas that need improvement. If the solution is fully consistent and accurate, state so explicitly. Otherwise, point out the issues that need to be addressed.

Problem and proposed solution:
"""

REFINE_SOLUTION_PROMPT = """
Based on the initial solution and the consistency check feedback, provide a refined and improved solution to the problem. Address any issues identified in the consistency check, ensure all steps are clearly explained, and present the final answer in a well-formatted manner.

Problem, initial solution, and consistency check feedback:
"""