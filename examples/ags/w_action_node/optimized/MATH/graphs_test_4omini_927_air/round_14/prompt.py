PRIME_FACTORIZATION_PROMPT = """
Given the problem statement, identify the target product value and perform its prime factorization. Return the result as a list of prime factors.

For example, if the target value is 715, the prime factorization would be [5, 11, 13].

Provide only the list of prime factors as the response, without any additional text or explanation.
"""

REFINE_SOLUTION_PROMPT = """
Review the given problem, the ensemble result of generated code solutions, and the prime factorization of the target product value. Provide a refined, step-by-step explanation of the solution, ensuring all calculations are correct and the final answer is clearly stated. If there are any errors in the code or its output, identify and correct them. Your response should be a complete, mathematically rigorous solution to the problem.

Important: Format your final answer using LaTeX notation enclosed in \boxed{}, for example: \boxed{42} or \boxed{x + y}.
"""