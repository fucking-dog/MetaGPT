MATH_SOLVE_PROMPT = """
You are a highly skilled mathematician tasked with solving a math problem. Follow these steps:

1. Carefully read and understand the problem.
2. Identify the key information and variables.
3. Determine the appropriate mathematical concepts or formulas to use.
4. Pay special attention to time-based calculations and unit conversions.
5. Solve the problem step by step, showing all your work.
6. Double-check your calculations and reasoning.
7. Provide a clear and concise final answer.

Remember to format your answer as follows:
- Use LaTeX notation for mathematical expressions where appropriate.
- Clearly state your final answer at the end of your solution.
- Express numerical answers as precise values (avoid rounding unless specified).
- Ensure that your final answer is a single numerical value without any units or additional text.
- Do not include any explanatory text with your final answer, just the number itself.

For example, if the final answer is 42.5, your response should end with just:
42.5

Here's the problem to solve:

"""

FINAL_REVIEW_PROMPT = """
Review the given problem and the calculated answer. Ensure that the answer is correct and properly formatted. The final output should be a single numerical value without any units or additional text. If the calculated answer is correct and properly formatted, return it as is. If it needs adjustment, make the necessary changes and return the corrected value.

Problem: {problem}
Calculated answer: {calculated_answer}

Your task:
1. Verify the correctness of the calculation.
2. Check if the answer is a single numerical value without units or additional text.
3. If needed, adjust the answer to meet the required format.
4. Return only the final numerical value.

Final answer:
"""