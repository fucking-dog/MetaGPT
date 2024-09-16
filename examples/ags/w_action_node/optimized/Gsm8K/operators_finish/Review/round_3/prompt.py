
REVIEW_PROMPT = """
Given the problem: {problem}

Please conduct a comprehensive review of the following solution:

{solution}

Your review should focus on the following aspects:
1. Correctness: Does the solution accurately address all parts of the problem?
2. Completeness: Are all steps of the solution clearly explained?
3. Efficiency: Is the approach used optimal for solving this problem?
4. Clarity: Is the solution presented in a clear and understandable manner?

After your analysis, provide a boolean review result:
- Return True if the solution satisfactorily addresses all aspects mentioned above.
- Return False if the solution falls short in any of these areas.

Additionally, provide brief feedback explaining your decision, highlighting strengths or areas for improvement.
"""

