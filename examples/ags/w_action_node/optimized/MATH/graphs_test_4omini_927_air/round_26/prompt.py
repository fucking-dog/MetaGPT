PRIME_FACTORIZATION_PROMPT = """
Given the problem statement, identify the target product value and perform a prime factorization of this value. If the problem doesn't explicitly mention a product value, infer it from the context. Present the prime factors in a clear, organized manner.

For example, if the target product value is 60, the prime factorization would be:
60 = 2 * 2 * 3 * 5

Provide only the prime factorization result without any additional explanation.
"""

GENERATE_MULTIPLE_APPROACHES_PROMPT = """
Based on the given problem, ensemble result, and prime factors, generate three distinct solution approaches. Each approach should use a different method or perspective to solve the problem. Present these approaches in a clear, step-by-step manner, highlighting the unique aspects of each method. Ensure that each approach is mathematically sound and directly addresses the problem statement.
"""

REFINE_SOLUTION_PROMPT = """
Review the given problem, the ensemble result of generated code solutions, the prime factorization, and the multiple solution approaches. Synthesize this information to provide a refined, step-by-step explanation of the solution. Ensure all calculations are correct, consider the strengths of each approach, and present a comprehensive solution that addresses the problem from multiple angles. The final answer should be clearly stated and mathematically rigorous.

Important: Format your final answer using LaTeX notation enclosed in \boxed{}, for example: \boxed{42} or \boxed{x + y}.
"""

ERROR_CHECK_PROMPT = """
Carefully review the problem statement and the refined solution. Check for any logical errors, calculation mistakes, or inconsistencies in the solution. If you find any errors, provide a corrected solution. If the solution is correct, simply confirm its accuracy.

Ensure that:
1. All calculations are mathematically correct.
2. The solution directly addresses the problem statement.
3. The final answer is clearly stated and formatted using LaTeX notation enclosed in \boxed{}.
4. The units of measurement are correct and consistent throughout the solution.
5. Any assumptions made are valid and clearly stated.

If corrections are needed, provide a complete, step-by-step solution. If the original solution is correct, state that it is accurate and restate the final answer.
"""