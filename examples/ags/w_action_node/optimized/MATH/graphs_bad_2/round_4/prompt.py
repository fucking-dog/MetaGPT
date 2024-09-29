INITIAL_ANALYSIS_PROMPT = """
Analyze the given mathematical problem. Identify key components, formulas, or calculations that might be needed to solve it. If possible, break down the problem into steps that could be solved using Python code.

Problem:
"""

SOLUTION_PROMPT = """
Based on the given problem and the Python calculation result, provide a detailed solution. Explain each step of your reasoning, incorporate the calculation result, and present the final answer clearly. Ensure your solution is mathematically sound and addresses all aspects of the problem.

Problem and calculation result:
"""

FALLBACK_SOLUTION_PROMPT = """
Solve the given mathematical problem step by step. Explain your reasoning clearly, show all necessary calculations, and provide a final answer. Be sure to consider all aspects of the problem and provide a comprehensive solution.

Problem:
"""