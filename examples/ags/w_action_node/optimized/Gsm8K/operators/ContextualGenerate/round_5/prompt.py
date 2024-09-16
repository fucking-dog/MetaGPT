
CONTEXTUAL_GENERATE_PROMPT = """
Solve the given mathematical problem step-by-step, utilizing the provided key information:

Problem: {problem}

Key Information: {context}

Solution Guidelines:
1. Analyze the problem and key information, identifying crucial mathematical concepts and formulas.
2. Outline a clear, efficient problem-solving strategy.
3. Present a concise yet comprehensive step-by-step solution.
4. Clearly explain each step, showing all necessary calculations and intermediate results.
5. Use precise mathematical notation and terminology throughout.
6. Ensure each step logically follows from the previous one.
7. If multiple approaches exist, choose the most efficient method.
8. Verify your solution by checking if it satisfies all given conditions and constraints.
9. Summarize the key findings or results concisely.

Your solution should be mathematically rigorous, logically structured, and as concise as possible while maintaining clarity.
"""

