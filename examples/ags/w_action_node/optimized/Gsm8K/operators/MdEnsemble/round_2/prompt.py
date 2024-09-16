
MD_ENSEMBLE_PROMPT = """
You are an expert judge evaluating solutions to a coding problem. Your task is to select the best solution from the given options.

Problem:
{problem}

Candidate Solutions:
{solutions}

Instructions:
1. Carefully analyze each solution for correctness, efficiency, and robustness.
2. Consider edge cases and potential issues in each implementation.
3. Evaluate the readability and maintainability of the code.
4. Choose the solution that best balances all these factors.

Your response should be a single letter (A, B, C, etc.) corresponding to the best solution.
"""

