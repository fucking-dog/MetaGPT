
CONTEXTUAL_GENERATE_PROMPT = """
Solve the given mathematical problem step-by-step, utilizing the provided key information:

Problem: {problem}

Key Information: {context}

Solution Guidelines:
1. Analyze the problem and key information thoroughly.
2. Identify relevant mathematical concepts, formulas, and theorems.
3. Develop a clear problem-solving strategy.
4. Present a detailed step-by-step solution:
   a. Start with given information and assumptions.
   b. Clearly state each step and its purpose.
   c. Explain your reasoning for each step.
   d. Show all calculations and intermediate results.
5. Use precise mathematical notation and terminology.
6. Verify your solution:
   a. Check if it satisfies all given conditions and constraints.
   b. Ensure the answer is reasonable and makes sense in the context.
7. If applicable, briefly discuss alternative approaches or methods.
8. Conclude with a concise summary of the key findings or results.

Aim for a comprehensive, logically structured, and mathematically rigorous solution that demonstrates clear understanding and problem-solving skills.
"""

