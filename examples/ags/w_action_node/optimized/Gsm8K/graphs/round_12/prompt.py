MATH_SOLVE_PROMPT = """
You are a highly skilled mathematician tasked with solving a math problem. Follow these steps:

1. Carefully read and understand the problem.
2. Identify the key information and variables.
3. Determine the appropriate mathematical concepts or formulas to use.
4. Solve the problem step by step, showing all your work.
5. Double-check your calculations and reasoning.
6. Provide a clear and concise final answer.

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

VERIFY_PROMPT = """
You are a meticulous math verifier. Your task is to verify the proposed answer to a given math problem. Follow these steps:

1. Carefully read the original problem.
2. Review the proposed answer.
3. Independently solve the problem, showing your work step-by-step.
4. Compare your solution with the proposed answer.
5. If the proposed answer is correct, return it as is.
6. If the proposed answer is incorrect, provide the correct answer.

Remember:
- Ensure your final answer is a single numerical value without units or additional text.
- Double-check all calculations for accuracy.
- If correcting the answer, use the same format as the original problem (i.e., same level of precision).

Here's the problem and proposed answer to verify:

"""