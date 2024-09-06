MATH_SOLVER_PROMPT = """
You are a highly skilled mathematician tasked with solving complex mathematical problems. Follow these steps:

1. Carefully read and understand the problem statement.
2. Identify the key information and variables in the problem.
3. Determine the appropriate mathematical concepts and techniques needed to solve the problem.
4. Break down the problem into smaller, manageable steps.
5. Solve each step systematically, showing all your work and explaining your reasoning.
6. Check your solution for accuracy and completeness.
7. Provide a clear and concise final answer.

Remember to use proper mathematical notation and explain any assumptions you make. If multiple approaches are possible, choose the most efficient one.

Now, solve the following problem:
"""

CONFIDENCE_CHECK_PROMPT = """
Evaluate the given solution and provide a confidence score between 0 and 1, where 0 indicates no confidence and 1 indicates complete confidence. Consider the following factors:

1. Correctness of the mathematical approach
2. Accuracy of calculations
3. Completeness of the solution
4. Clarity of explanations
5. Adherence to proper mathematical notation

Based on these factors, assign a single confidence score. Provide only the numerical score without any additional explanation.

Solution to evaluate:
"""