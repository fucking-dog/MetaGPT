MATH_SOLUTION_PROMPT = """
You are a skilled mathematician tasked with solving complex mathematical problems. Follow these steps:
1. Carefully read and understand the problem.
2. Identify the key information and unknowns.
3. Choose an appropriate problem-solving strategy.
4. Solve the problem step by step, showing all your work.
5. Double-check your calculations and reasoning.
6. Provide a clear and concise final answer.

Now, solve the given mathematical problem:
"""

CONFIDENCE_CHECK_PROMPT = """
Analyze the given solution and assess your confidence in its correctness. Consider the following:
1. The completeness of the solution.
2. The logical flow of the steps.
3. The correctness of the mathematical operations.
4. The alignment of the final answer with the problem requirements.

Based on your analysis, provide a confidence score between 0 and 1, where 0 is not confident at all and 1 is extremely confident. Only return the numeric score.
"""