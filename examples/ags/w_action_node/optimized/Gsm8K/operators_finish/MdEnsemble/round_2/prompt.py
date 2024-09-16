
MD_ENSEMBLE_PROMPT = """
Analyze the following problem and its proposed solutions:

Problem:
{problem}

Proposed Solutions:
{solutions}

Your task is to select the most appropriate solution. Consider these criteria:
1. Correctness: Does the solution fully address all aspects of the problem?
2. Efficiency: Is the solution optimized in terms of time and space complexity?
3. Readability: Is the code clear and well-structured?
4. Robustness: Does the solution handle edge cases and potential errors?
5. Scalability: Can the solution handle larger inputs or more complex scenarios?

Evaluate each solution against these criteria. Choose the solution that best balances all these aspects, with a primary focus on correctness and robustness. Provide your final decision by writing only the chosen solution letter.
"""

