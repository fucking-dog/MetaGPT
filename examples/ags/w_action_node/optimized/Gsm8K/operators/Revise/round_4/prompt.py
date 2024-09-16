
REVISE_PROMPT = """
Given the mathematical problem: {problem}

Original solution: {solution}

Review feedback: {feedback}

Please provide a revised solution by following these steps:
1. Analyze the original solution and review feedback critically.
2. Identify and prioritize key issues to address.
3. Revise the solution systematically, focusing on:
   - Correcting mathematical errors
   - Clarifying ambiguous explanations
   - Adding missing steps or reasoning
   - Improving logical flow
   - Using precise mathematical language and notation
4. If the original solution is correct and feedback suggests no changes, validate the solution's accuracy.
5. Ensure the revised solution is complete, accurate, and clearly presented.

Present your revised solution concisely and logically, highlighting any significant changes or improvements made.
"""

