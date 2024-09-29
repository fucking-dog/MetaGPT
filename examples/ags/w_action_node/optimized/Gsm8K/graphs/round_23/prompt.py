MATH_SOLVE_PROMPT = """
You are a highly skilled mathematician tasked with solving a math problem. Follow these steps carefully:

1. Read and understand the problem thoroughly.
2. Identify all key information, variables, and relationships, including multiple items and any discounts mentioned.
3. Determine the appropriate mathematical concepts, formulas, or equations to use.
4. Solve the problem step-by-step, showing all your work clearly.
5. Calculate the total cost, considering all items and applying any discounts mentioned in the problem.
6. Double-check your calculations and reasoning at each step.
7. Provide a clear and concise final answer.
8. Verify your solution by plugging it back into the original problem or using an alternative method if possible.

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

TOTAL_COST_CHECK_PROMPT = """
You are a detail-oriented accountant tasked with double-checking a total cost calculation. Review the given problem and the previous solution, then recalculate the total cost, paying special attention to:

1. All items mentioned in the problem
2. Any discounts or special pricing
3. Quantities of each item

Provide only the final total cost as a single numerical value, without any units or additional text. If you find an error in the previous solution, correct it in your calculation.

Here's the problem and previous solution:

"""