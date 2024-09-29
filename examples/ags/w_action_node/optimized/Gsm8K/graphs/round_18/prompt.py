MATH_SOLVE_PROMPT = """
You are a highly skilled mathematician tasked with solving a math problem. Follow these steps:

1. Carefully read and understand the problem.
2. Identify the key information and variables.
3. Determine the appropriate mathematical concepts or formulas to use.
4. Solve the problem step by step, showing all your work.
5. Pay special attention to unit conversions (e.g., inches to feet, minutes to hours).
6. For time-based problems, convert all time units to a single unit (preferably hours or minutes).
7. For problems involving money, ensure all calculations are in the same currency unit.
8. Double-check your calculations and reasoning, especially for unit conversions and complex calculations.
9. Provide a clear and concise final answer.

Remember to format your answer as follows:
- Use LaTeX notation for mathematical expressions where appropriate.
- Clearly state your final answer at the end of your solution.
- Express numerical answers as precise values (avoid rounding unless specified).
- Ensure that your final answer is a single numerical value without any units or additional text.
- Do not include any explanatory text with your final answer, just the number itself.

For example, if the final answer is 42.5 hours, your response should end with just:
42.5

Here's the problem to solve:

"""