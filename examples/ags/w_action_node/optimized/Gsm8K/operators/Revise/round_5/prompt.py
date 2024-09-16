
REVISE_PROMPT = """
Given the mathematical problem: {problem}

Original solution: {solution}

Review feedback: {feedback}

Please provide a revised solution by following these steps:
1. Carefully analyze the original solution and review feedback.
2. Identify key issues and areas for improvement.
3. Revise the solution, focusing on:
   - Correcting mathematical errors
   - Clarifying explanations
   - Adding missing steps or reasoning
   - Improving logical flow
   - Using precise mathematical language and notation
4. If the original solution is correct and feedback suggests no changes, validate and confirm its accuracy.
5. Ensure the revised solution is complete, accurate, and clearly presented.

Present your revised solution concisely and logically, emphasizing any significant changes or improvements. If no changes are needed, briefly explain why the original solution is correct and complete.
"""

