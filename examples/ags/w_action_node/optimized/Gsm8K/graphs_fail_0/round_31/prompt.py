MATH_SOLUTION_PROMPT = """
You are a highly skilled mathematician tasked with solving complex mathematical problems. Follow these steps:

1. Carefully read and understand the given problem.
2. Identify the key information and variables in the problem.
3. Determine the appropriate mathematical concepts and techniques needed to solve the problem.
4. Break down the problem into smaller, manageable steps.
5. Solve each step systematically, showing all your work and explaining your reasoning.
6. Check your solution for accuracy and consistency.
7. Provide a clear and concise final answer.

Remember to use proper mathematical notation and explain any assumptions you make. If multiple approaches are possible, choose the most efficient one and briefly explain why you selected it.

Now, solve the following problem:

"""

CONFIDENCE_CHECK_PROMPT = """
Evaluate the confidence level of the provided solution on a scale from 0 to 1, where 0 represents no confidence and 1 represents absolute certainty. Consider the following factors:

1. Completeness of the solution
2. Logical coherence of the steps
3. Adherence to mathematical principles
4. Clarity of explanations
5. Potential for errors or oversights

Based on these factors, provide a single number between 0 and 1 representing your confidence in the solution. Do not include any additional text or explanations in your response.

Solution to evaluate:

"""