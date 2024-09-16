
REVIEW_PROMPT = """
Carefully analyze the following problem and its proposed solution:

Problem: {problem}

Proposed Solution: {solution}

Your task is to review this solution based on the following criteria:
1. Accuracy: Does the solution correctly address all aspects of the problem?
2. Completeness: Does the solution cover all necessary steps or components?
3. Clarity: Is the solution presented in a clear and understandable manner?
4. Efficiency: If applicable, is the solution efficient in terms of time or resources?

Provide your review as follows:
1. A boolean value (True/False) indicating whether the solution is satisfactory overall.
2. A brief explanation of your decision, highlighting strengths or areas for improvement.

Focus on the quality and correctness of the solution rather than its formatting or presentation style.
"""

