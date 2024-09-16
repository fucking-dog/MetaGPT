
MD_ENSEMBLE_PROMPT = """
Analyze the following problem:
{problem}

You have been provided with multiple candidate solutions:
{solutions}

Your task is to select the optimal solution for this problem. Consider the following criteria:
1. Correctness: The solution must fully address all aspects of the problem.
2. Robustness: The solution should handle various input scenarios and edge cases.
3. Efficiency: While not the primary factor, consider the solution's performance.
4. Readability: The code should be clear and well-structured.
5. Scalability: The solution should work for larger inputs if applicable.

Evaluate each solution against these criteria. If a solution fails to meet any of these criteria, it should not be selected.

Provide your final decision by writing only the chosen solution letter.
"""

