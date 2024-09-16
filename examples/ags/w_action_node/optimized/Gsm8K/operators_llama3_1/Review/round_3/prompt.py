
REVIEW_PROMPT = """
As an expert reviewer, your task is to critically evaluate the given solution for the presented problem. Consider the following criteria:

1. Accuracy: Does the solution correctly address all aspects of the problem?
2. Completeness: Is every step of the problem-solving process accounted for?
3. Clarity: Is the solution explained in a logical and easy-to-follow manner?
4. Efficiency: If relevant, does the solution use an optimal approach?

Problem: {problem}

Proposed Solution: {solution}

Provide your assessment as follows:
1. A boolean value (True/False) indicating if the solution meets all criteria satisfactorily.
2. A concise explanation of your decision, highlighting strengths and/or areas needing improvement.

Focus solely on the solution's quality and correctness, disregarding formatting or presentation style.
"""

