SOLVE_PROMPT = """
Solve the given math problem step by step. Show your work clearly and provide a final answer.
After solving, extract the numerical answer and present it as follows:
Final Answer: [numerical value]

Solve it now:
"""

EXTRACT_ANSWER_PROMPT = """
Extract only the numerical value from the given solution. If there are multiple numerical values, extract the one labeled as 'Final Answer'. Return only the numerical value without any additional text or symbols.
"""

FINAL_ANSWER_PROMPT = """
Review the problem, the initial solution, and the verification result. Provide the final, correct answer as a single numerical value without any additional text or explanation. Ensure the answer is accurate based on all the information provided.

Return the answer in this format:
[numerical value]
"""