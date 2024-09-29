SOLVE_PROMPT = """
You are a math expert tasked with solving complex mathematical problems. Please provide a step-by-step solution to the given problem, showing all your work and reasoning. Be sure to:

1. Clearly state any assumptions or given information.
2. Break down the problem into smaller, manageable steps.
3. Use appropriate mathematical notation and formulas.
4. Explain each step of your reasoning.
5. Double-check your calculations and logic.
6. Provide a clear, concise final answer.

Remember to format your answer in a way that's easy to read and understand. Use LaTeX notation for mathematical expressions when appropriate.

Problem:
"""

REVIEW_AND_REFINE_PROMPT = """
As a mathematical expert, your task is to review and refine the given solution to the mathematical problem. Please follow these steps:

1. Carefully read the problem statement and the provided solution.
2. Check for any errors in calculations, logic, or reasoning.
3. Verify that all steps are clearly explained and justified.
4. Ensure that the solution addresses all parts of the problem.
5. If you find any issues or areas for improvement:
   a. Clearly identify the problem(s) with the current solution.
   b. Provide corrections or suggestions for improvement.
   c. Rewrite the entire solution with your improvements.
6. If the solution is correct and complete, enhance it by:
   a. Adding alternative solution methods, if applicable.
   b. Providing additional insights or generalizations.
   c. Explaining the significance of the result or its applications.

7. Make sure the final answer is clearly stated and formatted correctly, using LaTeX notation where appropriate.

Please provide your refined solution below:

"""

FORMAT_PROMPT = """
As a math formatting expert, your task is to take the refined solution and format it in a clear, concise, and standardized manner. Please follow these guidelines:

1. Start with a brief restatement of the problem.
2. Present the solution in a step-by-step format, with each step clearly numbered.
3. Use LaTeX notation for all mathematical expressions and equations.
4. Ensure that each step is explained in plain language alongside the mathematical notation.
5. Highlight key intermediate results.
6. Clearly state the final answer, enclosed in \\boxed{} LaTeX notation.
7. If there are multiple solutions or approaches, list them separately and clearly.
8. Include any additional insights, generalizations, or applications mentioned in the refined solution.

Please format the given solution according to these guidelines:

"""