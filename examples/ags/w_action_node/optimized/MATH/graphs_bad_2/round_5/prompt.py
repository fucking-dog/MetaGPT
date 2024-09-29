INITIAL_ANALYSIS_PROMPT = """
Analyze the given mathematical problem. Identify key components, formulas, or calculations that might be needed to solve it. If possible, break down the problem into steps that could be solved using Python code.

Problem:
"""

PROBLEM_TYPE_ANALYSIS_PROMPT = """
Based on the given problem and initial analysis, determine the type of mathematical problem and suggest a solution strategy. Consider various problem-solving techniques and mathematical concepts that might be applicable.

Problem and initial analysis:
"""

SOLUTION_PROMPT = """
Based on the given problem, Python calculation result, and problem type analysis, provide a detailed solution. Explain each step of your reasoning, incorporate the calculation result, and present the final answer clearly. Ensure your solution is mathematically sound and addresses all aspects of the problem.

Problem, calculation result, and problem type analysis:
"""

FALLBACK_SOLUTION_PROMPT = """
Solve the given mathematical problem step by step, considering the problem type analysis. Explain your reasoning clearly, show all necessary calculations, and provide a final answer. Be sure to consider all aspects of the problem and provide a comprehensive solution.

Problem and problem type analysis:
"""