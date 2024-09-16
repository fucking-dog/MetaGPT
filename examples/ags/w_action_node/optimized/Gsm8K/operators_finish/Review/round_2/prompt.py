
REVIEW_PROMPT = """
Carefully analyze the following problem and its proposed solution:

Problem: {problem}

Proposed Solution: {solution}

Your task is to review this solution based on the following criteria:
1. Correctness: Is the solution mathematically accurate?
2. Completeness: Does it fully address all aspects of the problem?
3. Clarity: Is the solution clear and easy to understand?
4. Efficiency: Is it the most efficient approach to solve the problem?

After your analysis, provide your review as follows:
1. A boolean value (True/False) indicating whether the solution satisfactorily meets all the above criteria.
2. A brief explanation of your decision, highlighting strengths or areas for improvement.
"""

