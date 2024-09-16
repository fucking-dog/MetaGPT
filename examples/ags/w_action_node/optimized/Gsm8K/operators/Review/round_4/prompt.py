
REVIEW_PROMPT = """
Carefully evaluate the given solution for this mathematical problem: {problem}

Assess the solution based on these critical criteria:
1. Mathematical Accuracy: Is every calculation and step mathematically correct?
2. Completeness: Does the solution address all parts of the problem without omissions?
3. Clarity of Explanation: Is the solution's reasoning clear, logical, and easy to follow?
4. Efficiency of Approach: Is this the most optimal or elegant method to solve the problem?

Thoroughly analyze each criterion. Return True only if ALL criteria are fully satisfied. Return False if any criterion is not met.

Provide concise, specific feedback highlighting:
- Strengths of the solution
- Areas needing improvement (if any)
- Suggestions for enhancement (if applicable)

Your evaluation should be thorough yet concise, focusing on the mathematical validity and quality of the solution.
"""

