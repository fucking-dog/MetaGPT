STEP_SOLVE_PROMPT = """
You are an expert math problem solver. Your task is to solve the given math problem step by step. Follow these guidelines:

1. Read the problem carefully and identify the key information.
2. Break down the problem into smaller steps.
3. Show your work for each step, including any calculations.
4. Use clear and concise language to explain your reasoning.
5. Double-check your calculations and logic.
6. If the problem involves time, pay extra attention to unit conversions and relationships between different time units.
7. For problems with multiple conditions or scenarios, ensure you account for all of them in your solution.
8. When dealing with percentages, be careful to calculate the correct base amount.
9. If the question asks for a specific type of answer (e.g., number of people), make sure your final answer matches that type.

Solve the following problem step by step:

"""

FINAL_ANSWER_PROMPT = """
Based on the verified step-by-step solution provided, extract the final answer to the problem. Make sure to:

1. Clearly state the final answer.
2. Ensure the answer is in the correct format (e.g., number of people, amount of money, etc.) as requested in the original problem.
3. Double-check that the answer logically follows from the verified solution.
4. If the answer involves decimals, round to two decimal places unless otherwise specified.
5. Include the appropriate units if applicable (e.g., dollars, days, etc.).

Provide only the final answer without any additional explanation:

"""