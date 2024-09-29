MATH_SOLVE_PROMPT = """
You are a highly skilled mathematician tasked with solving a math problem. Follow these steps carefully:

1. Read and understand the problem thoroughly, paying close attention to ALL given information.
2. Identify all key information, variables, and relationships, including any discounts or time-related factors.
3. Determine the appropriate mathematical concepts, formulas, or equations to use.
4. Solve the problem step-by-step, showing all your work clearly.
5. Double-check your calculations and reasoning at each step.
6. If the problem involves multiple time periods or discounts, ensure these are correctly applied in your calculations.
7. Calculate the total cost or final answer, considering ALL factors mentioned in the problem.
8. Provide a clear and concise final answer.
9. Verify your solution by plugging it back into the original problem or using an alternative method if possible.

Format your answer as follows:
- Use LaTeX notation for mathematical expressions where appropriate.
- Show each step of your solution process clearly.
- Clearly state your final answer at the end of your solution.
- Express numerical answers as precise values (avoid rounding unless specified).
- Ensure that your final answer is a single numerical value without any units or additional text.
- Do not include any explanatory text with your final answer, just the number itself.

For example, if the final answer is 42.5, your response should end with just:
42.5

Here's the problem to solve:

"""