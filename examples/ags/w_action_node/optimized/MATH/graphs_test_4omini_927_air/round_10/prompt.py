VERIFY_MATH_CORRECTNESS_PROMPT = """
Carefully review the given problem and the ensemble result. Verify the mathematical correctness of the solution by following these steps:

1. Check if all mathematical operations (addition, subtraction, multiplication, division, exponentiation, etc.) are performed correctly.
2. Verify that all algebraic manipulations are valid and follow proper mathematical rules.
3. Ensure that any simplifications or reductions are done correctly.
4. Check for any numerical errors or inconsistencies in the calculations.
5. Verify that any mathematical properties or theorems used are applied correctly.

If you find any mathematical errors, provide a corrected version of the calculations. If the solution is mathematically correct, confirm its correctness.

Your response should be concise and focus on the mathematical aspects of the solution. If corrections are needed, briefly explain the changes made.

Important: Do not change the overall approach or structure of the solution at this stage. Focus only on mathematical correctness.
"""

REFINE_SOLUTION_PROMPT = """
Review the given problem and the verified result. Provide a refined, step-by-step explanation of the solution, ensuring all calculations are correct and the final answer is clearly stated. If there are any errors in the code or its output, identify and correct them. Your response should be a complete, mathematically rigorous solution to the problem.

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

SIMPLIFY_AND_FORMAT_PROMPT = """
Review the verified solution and perform a final simplification and formatting check. Follow these steps:

1. Ensure that the final answer is in its simplest form (e.g., fractions are reduced, radicals are simplified).
2. Check that the answer is correctly formatted using LaTeX notation and enclosed in \boxed{}.
3. If the answer involves fractions, ensure they are properly formatted (e.g., \frac{numerator}{denominator}).
4. For complex expressions, use appropriate LaTeX commands to improve readability (e.g., \sqrt{}, \cdot for multiplication).
5. If multiple answers are possible, separate them clearly (e.g., \boxed{x_1 = 3, x_2 = -3}).

Provide the final, simplified, and correctly formatted answer. If no changes are needed, restate the original answer.

Your response should be concise and focus only on the final answer. Do not include explanations or steps unless absolutely necessary for clarity.

Important: The final answer must always be formatted using LaTeX notation enclosed in \boxed{}.
"""