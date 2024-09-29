PRIME_FACTORIZATION_PROMPT = """
Given a math problem involving finding a word with a specific product value, perform the following steps:
1. Extract the target product value from the problem description.
2. Calculate the prime factorization of this value.
3. List the prime factors and their corresponding letter values (A=1, B=2, C=3, ..., Z=26).
4. Provide this information in a clear, concise format.

Your response should only include the prime factorization and corresponding letter values, without solving the entire problem.
"""

REFINE_SOLUTION_PROMPT = """
Review the given problem, the ensemble result of generated code solutions, and the prime factorization. Provide a refined, step-by-step explanation of the solution, ensuring all calculations are correct and the final answer is clearly stated. If there are any errors in the code or its output, identify and correct them. Your response should be a complete, mathematically rigorous solution to the problem.

Important: Format your final answer using LaTeX notation enclosed in \boxed{}, for example: \boxed{42} or \boxed{x + y}.
"""