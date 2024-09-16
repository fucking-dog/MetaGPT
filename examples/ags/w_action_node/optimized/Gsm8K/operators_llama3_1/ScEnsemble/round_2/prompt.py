
SC_ENSEMBLE_PROMPT = """
You are an expert in evaluating mathematical solutions. Your task is to analyze multiple solutions to the following problem:

{problem}

Here are the proposed solutions:

{solutions}

Your objective is to:
1. Carefully examine each solution for correctness and logical consistency.
2. Identify the solution that appears most frequently or shares the most common elements with other solutions.
3. If there's a tie, select the solution with the most detailed and clear explanation.
4. Choose the solution that best aligns with established mathematical principles and problem-solving techniques.

Provide your answer as a single letter corresponding to the chosen solution, without any additional explanation or commentary.
"""

