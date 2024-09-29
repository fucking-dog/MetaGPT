SOLVE_PROMPT = """
You are a mathematical problem solver. Your task is to solve the given problem using a {approach} approach. Follow these guidelines:

1. Clearly state the problem and identify the key information.
2. Break down the problem into smaller, manageable steps.
3. Use appropriate mathematical notation and formulas.
4. Explain each step of your reasoning clearly.
5. If using a visual approach, describe or sketch any diagrams or visual aids.
6. If using an algebraic approach, clearly define variables and show equation manipulations.
7. Double-check your calculations and logic.
8. Provide a clear, concise final answer, preferably in a boxed format like this: \\boxed{{final answer}}.

Problem to solve:
"""

REVIEW_PROMPT = """
Review the given solution to the mathematical problem. Your task is to:

1. Check if the solution is correct and complete.
2. Identify any errors or missing steps in the reasoning.
3. Verify all calculations and mathematical operations.
4. Ensure that the solution uses appropriate mathematical notation and formulas.
5. Check if the solution addresses all parts of the problem.
6. Suggest improvements or alternative approaches if applicable.
7. If improvements are needed, provide a revised solution following the same guidelines as the original solver.
8. If the solution is correct and complete, confirm it and restate the final answer.

Always end your review with a final answer in a boxed format like this: \\boxed{{final answer}}.

Problem and current solution:
"""

VERIFY_PROMPT = """
Perform a self-consistency check on the given final solution to the mathematical problem. Your task is to:

1. Restate the problem and the final answer.
2. Verify that the final answer is consistent with the problem statement.
3. If possible, use a different method to solve the problem and compare the results.
4. Check for any logical inconsistencies or mathematical impossibilities in the solution.
5. Ensure that the units and dimensions are correct and consistent throughout the solution.
6. If any inconsistencies are found, explain them and provide a corrected final answer.
7. If the solution passes all checks, confirm its validity.

Always end your verification with the final, verified answer in a boxed format like this: \\boxed{{final answer}}.

Problem and final solution:
"""