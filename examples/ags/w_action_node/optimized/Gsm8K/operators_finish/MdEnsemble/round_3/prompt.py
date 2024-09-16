
MD_ENSEMBLE_PROMPT = """
Analyze the given problem and its proposed solutions:

Problem:
{problem}

Proposed Solutions:
{solutions}

Your task is to select the most appropriate solution based on the following criteria:

1. Correctness: Does the solution fully and accurately address all aspects of the problem?
2. Efficiency: Is the approach optimized for time and space complexity?
3. Clarity: Is the solution presented in a clear, well-structured manner?
4. Robustness: Does it handle potential edge cases and error scenarios?
5. Scalability: Can the solution adapt to larger inputs or more complex variations of the problem?

Evaluate each solution against these criteria, prioritizing correctness and robustness. Consider the trade-offs between different aspects, and choose the solution that best balances all criteria while ensuring the problem is solved correctly.

Provide your final decision by writing only the chosen solution letter.
"""

