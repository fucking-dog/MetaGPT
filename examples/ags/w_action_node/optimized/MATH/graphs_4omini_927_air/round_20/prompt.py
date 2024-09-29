PRIME_FACTORIZATION_PROMPT = """
Given the problem statement, identify the target product value and perform a prime factorization of this value. If the problem doesn't explicitly mention a product value, infer it from the context. Present the prime factors in a clear, organized manner.

For example, if the target product value is 60, the prime factorization would be:
60 = 2 * 2 * 3 * 5

Provide only the prime factorization result without any additional explanation.
"""

REFINE_SOLUTION_PROMPT = """
Review the given problem, the ensemble result of generated code solutions, and the prime factorization. Provide a refined, step-by-step explanation of the solution, ensuring all calculations are correct and the final answer is clearly stated. If there are any errors in the code or its output, identify and correct them. Your response should be a complete, mathematically rigorous solution to the problem.

Important: Format your final answer using LaTeX notation enclosed in \boxed{}, for example: \boxed{42} or \boxed{x + y}.
"""