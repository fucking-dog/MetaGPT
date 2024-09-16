
MD_ENSEMBLE_PROMPT = """
You are an expert judge in a coding competition. Your task is to evaluate multiple solutions to a given problem and select the best one. The problem is:

{problem}

Below are the candidate solutions:
{solutions}

Your objective is to choose the most suitable solution based on the following criteria:
1. Correctness: The solution must fully solve the problem without errors.
2. Robustness: The solution should handle various input cases and edge scenarios.
3. Readability: The code should be clear and easy to understand.
4. Efficiency: While not the primary factor, consider the solution's performance if all other aspects are equal.

Analyze each solution carefully, considering its strengths and weaknesses. Then, provide your final decision by writing only the letter of the chosen solution.
"""

