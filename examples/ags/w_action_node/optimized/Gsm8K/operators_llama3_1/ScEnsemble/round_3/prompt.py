
SC_ENSEMBLE_PROMPT = """
As a mathematical solution evaluator, your task is to analyze multiple solutions for this problem:

{problem}

Proposed solutions:

{solutions}

Your evaluation process:
1. Assess each solution's correctness and logical consistency.
2. Identify the most frequent or common solution elements.
3. For tied solutions, prioritize the one with the clearest, most detailed explanation.
4. Select the solution that best adheres to mathematical principles and problem-solving methods.

Respond with a single letter (A, B, C, etc.) corresponding to your chosen solution.
"""

