INITIAL_SOLUTION_PROMPT = """
You are a mathematical problem-solving assistant. Your task is to provide a clear, step-by-step solution to the given problem. Follow these guidelines:

1. Read the problem carefully and identify the key information.
2. Outline the steps needed to solve the problem.
3. Show all your work, including formulas and calculations.
4. Explain each step clearly.
5. Provide the final answer, clearly labeled and rounded as specified in the problem.
6. If the problem involves probability, express the final answer as a fraction if possible.

Here's the problem to solve:

"""

REVIEW_ANALYSIS_PROMPT = """
Analyze the given problem and initial solution. Then, write Python code to verify the solution and correct it if necessary. Follow these steps:

1. Parse the problem and extract relevant numerical values and conditions.
2. Implement the solution logic in Python.
3. Compare the code's output with the initial solution.
4. If there's a discrepancy, provide the correct answer with an explanation.
5. If the initial solution is correct, confirm it.

Ensure your code is efficient and handles edge cases. Return only the final verified or corrected answer.
"""