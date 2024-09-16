
REVIEW_PROMPT = """
Evaluate the given solution for this mathematical problem: {problem}

Assess the solution based on these criteria:
1. Mathematical Accuracy: Are all calculations and steps correct?
2. Completeness: Does it address all parts of the problem?
3. Clarity: Is the reasoning clear and logical?
4. Efficiency: Is it the most optimal method?

Analyze each criterion thoroughly. Return True only if ALL criteria are fully satisfied. Otherwise, return False.

Provide concise feedback on:
- Solution strengths
- Areas for improvement (if any)
- Enhancement suggestions (if applicable)

Focus on mathematical validity and solution quality in your evaluation.
"""

