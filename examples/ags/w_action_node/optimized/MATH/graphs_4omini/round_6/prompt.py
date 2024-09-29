VERIFY_ENSEMBLE_PROMPT = """
Carefully review the given problem and the ensemble result of generated code solutions. Verify the mathematical accuracy and completeness of the ensemble result. If the result is correct and complete, start your response with "Correct:". If there are any errors or missing steps, start your response with "Incorrect:" and provide a detailed explanation of the issues found.
"""

REFINE_SOLUTION_PROMPT = """
Review the given problem and the ensemble result or corrected solution. Provide a refined, step-by-step explanation of the solution, ensuring all calculations are correct and the final answer is clearly stated. Your response should be a complete, mathematically rigorous solution to the problem.

Important: Format your final answer using LaTeX notation enclosed in \boxed{}, for example: \boxed{42} or \boxed{x + y}.
"""

VERIFY_SOLUTION_PROMPT = """
Carefully review the given problem and the refined solution. Verify the correctness of the solution, checking for mathematical accuracy, logical consistency, and completeness. If the solution is correct, start your response with "Correct:". If there are any errors or improvements needed, start your response with "Incorrect:" and provide a detailed explanation of the issues found.
"""

CORRECT_SOLUTION_PROMPT = """
Given the problem, the ensemble result or refined solution, and the verification result, provide a corrected and improved solution. Address all issues mentioned in the verification result and ensure the solution is mathematically accurate, logically consistent, and complete. Present the solution in a clear, step-by-step manner.

Important: Format your final answer using LaTeX notation enclosed in \boxed{}, for example: \boxed{42} or \boxed{x + y}.
"""