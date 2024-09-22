ANALYZE_PROMPT = """
Analyze the given math problem and extract key numerical values and relationships. Identify important information that will be crucial for solving the problem. Present your analysis in a clear, structured format.

Problem to analyze:
"""

SOLVE_PROMPT = """
Solve the given math problem step by step, using the provided analysis. Show your work clearly and provide a final answer.
After solving, extract the numerical answer and present it as follows:
Final Answer: [numerical value]

Problem and Analysis:
"""

REVIEW_PROMPT = """
Review the problem, initial solution, and verification. Identify any errors or discrepancies. If necessary, recalculate the answer. Provide a final, corrected solution with clear reasoning.

Problem:
{problem}

Initial Solution:
{initial_solution}

Verification:
{verification}

Please review and provide the corrected solution:
"""