ANALYSIS_PROMPT = """
Analyze the given math problem. Break it down into steps and provide a clear explanation of the solution approach. Include any formulas or equations that need to be used.

"""

FINAL_SOLUTION_PROMPT = """
Based on the problem, analysis, and code solution provided, generate a final answer. Ensure that the answer is a single numerical value without any units or explanations. If the code solution provides a correct numerical answer, use that. Otherwise, use the analysis to derive the correct answer.

"""