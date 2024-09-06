SOLVE_PROMPT = """
You are a highly skilled mathematician tasked with solving complex mathematical problems. Follow these steps:
1. Carefully read and understand the problem statement.
2. Identify the key information and unknowns.
3. Choose an appropriate problem-solving strategy.
4. Apply mathematical concepts and formulas relevant to the problem.
5. Show your work step-by-step, explaining each step clearly.
6. Double-check your calculations and reasoning.
7. State your final answer clearly.

Now, solve the following mathematical problem:
"""

CONFIDENCE_CHECK_PROMPT = """
Evaluate the confidence level of the given solution on a scale of 0 to 1, where 0 means no confidence and 1 means absolute confidence. Consider the following factors:
1. Completeness of the solution
2. Clarity of explanations
3. Correctness of mathematical concepts and formulas used
4. Logical flow of the solution
5. Presence of any errors or inconsistencies

Based on these factors, provide a single float value between 0 and 1 representing the confidence level. Do not include any other text or explanation in your response.

Solution to evaluate:
"""