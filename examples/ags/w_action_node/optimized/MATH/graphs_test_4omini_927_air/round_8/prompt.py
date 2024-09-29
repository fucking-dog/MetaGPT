REFINE_SOLUTION_PROMPT = """
Review the given problem and the ensemble result of generated code solutions. Provide a refined, step-by-step explanation of the solution, ensuring all calculations are correct and the final answer is clearly stated. If there are any errors in the code or its output, identify and correct them. Your response should be a complete, mathematically rigorous solution to the problem.

Important: Format your final answer using LaTeX notation enclosed in \boxed{}, for example: \boxed{42} or \boxed{x + y}.
"""

VERIFY_SOLUTION_PROMPT = """
Carefully review the given problem and the refined solution. Verify the correctness of the solution by following these steps:

1. Check if all the given information in the problem is used correctly in the solution.
2. Verify that each step in the solution logically follows from the previous one.
3. Ensure that all calculations are accurate.
4. Confirm that the final answer addresses the specific question asked in the problem.
5. Verify that the final answer is formatted correctly using LaTeX notation enclosed in \boxed{}.

If you find any errors or inconsistencies, provide a corrected solution. If the solution is correct, restate the final answer.

Your response should be concise and focus on the verification process and the final answer. If corrections are needed, briefly explain the changes made.

Important: The final answer must be formatted using LaTeX notation enclosed in \boxed{}, for example: \boxed{42} or \boxed{x + y}.
"""

FINAL_CHECK_PROMPT = """
Perform a final check on the verified solution. Ensure that:

1. The solution is complete and addresses all aspects of the problem.
2. All mathematical expressions are in their simplest form.
3. The final answer is correctly formatted using LaTeX notation enclosed in \boxed{}.
4. Any fractions are reduced to their lowest terms.
5. Any radicals are simplified as much as possible.
6. The solution uses appropriate mathematical notation and terminology.

If any improvements or simplifications are needed, make them and provide a brief explanation of the changes. If the solution is already optimal, simply restate the final answer.

Your response should be concise and focus on the final, simplified answer. 

Important: The final answer must be formatted using LaTeX notation enclosed in \boxed{}, for example: \boxed{42} or \boxed{x + y}.
"""