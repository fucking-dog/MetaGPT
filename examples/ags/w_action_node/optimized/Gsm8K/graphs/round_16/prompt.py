EXTRACT_KEY_INFO_PROMPT = """
You are an expert at analyzing math problems. Your task is to extract and summarize the key information from the given problem. Follow these guidelines:

1. Identify all numerical values and their associated units.
2. Recognize any mathematical operations or relationships mentioned (e.g., percentages, fractions, multiples).
3. Note any time-related information (days, weeks, hours, etc.).
4. Identify any conditions or scenarios that need to be considered.
5. Summarize the main question or what needs to be calculated.

Provide a concise summary of the key information in bullet points.

Extract key information from the following problem:

"""

SOLVE_PROMPT = """
You are an expert math problem solver. Your task is to solve the given math problem step by step, using the provided key information. Follow these guidelines:

1. Review the problem and the extracted key information carefully.
2. Break down the problem into smaller steps.
3. Show your work for each step, including any calculations.
4. Use clear and concise language to explain your reasoning.
5. Double-check your calculations and logic.
6. Provide a final answer, clearly stated and highlighted.
7. Ensure your solution addresses all aspects of the problem, including multiple conditions or scenarios if present.
8. Pay special attention to unit conversions, especially with time-related problems.
9. When dealing with percentages, carefully calculate the correct base amount.
10. Make sure your final answer matches the type requested in the question (e.g., number of people, total cost).
11. For time-based problems, be extra careful with calculations involving hours and minutes.
12. When dealing with sequences or patterns, verify that your solution accounts for all steps or iterations.

Solve the following problem using the provided key information:

"""