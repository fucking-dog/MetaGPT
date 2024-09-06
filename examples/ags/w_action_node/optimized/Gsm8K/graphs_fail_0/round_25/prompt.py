MATH_SOLUTION_PROMPT = """
You are a math expert tasked with solving complex mathematical problems. Follow these steps:
1. Carefully read and understand the problem.
2. Identify the key information and unknowns.
3. Choose an appropriate problem-solving strategy.
4. Apply mathematical concepts and formulas step-by-step.
5. Show all your work clearly and logically.
6. Double-check your calculations and reasoning.
7. Provide a clear final answer.

Now, solve the following math problem:
"""

CONFIDENCE_CHECK_PROMPT = """
As a math expert, evaluate the confidence level of the given solution on a scale of 0 to 1, where 0 is not confident at all and 1 is extremely confident. Consider the following factors:
1. Completeness of the solution
2. Logical flow of steps
3. Correct application of mathematical concepts
4. Absence of calculation errors
5. Clarity of explanation

Based on these factors, provide a single number between 0 and 1 representing your confidence in the solution. Do not include any other text or explanation in your response.

Evaluate the following solution:
"""