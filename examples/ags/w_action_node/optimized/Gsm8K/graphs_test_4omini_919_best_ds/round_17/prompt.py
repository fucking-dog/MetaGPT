SOLVE_PROMPT = """
Solve the given math problem step by step. Show your work and clearly state the final answer.

1. Read the problem carefully and identify the key information.
2. Determine the appropriate mathematical operations needed to solve the problem.
3. Perform the calculations step by step, showing your work.
4. Clearly state the final answer, including the appropriate units if applicable.
5. Double-check your calculations for accuracy.

Provide your solution below:
"""

ALTERNATIVE_SOLVE_PROMPT = """
Solve the given math problem using a different approach or method than you might typically use. Show your work step by step and clearly state the final answer.

1. Read the problem carefully and identify the key information.
2. Think of an alternative method or approach to solve the problem.
3. Perform the calculations step by step, showing your work.
4. Clearly state the final answer, including the appropriate units if applicable.
5. Verify your solution by checking if it makes sense in the context of the problem.

Provide your alternative solution below:
"""

EDGE_CASE_PROMPT = """
Analyze the given math problem for potential edge cases, special scenarios, or hidden complexities that might affect the solution. Consider the following:

1. Are there any implicit assumptions in the problem that need to be addressed?
2. Are there any extreme or boundary conditions that could change the approach to solving the problem?
3. Are there any special rules or exceptions that apply to this type of problem?
4. Could there be multiple interpretations of the problem statement?
5. Are there any potential pitfalls or common mistakes to avoid when solving this problem?

Provide your edge case analysis below:
"""

BREAKDOWN_PROMPT = """
Break down the given problem, solutions, and edge case analysis into clear, concise steps. Identify the key components of the problem and the mathematical operations used in each solution. Provide a structured analysis that can be easily validated programmatically.

1. Identify the important variables and values in the problem.
2. List the mathematical operations used in each solution.
3. Break down each solution into individual calculation steps.
4. Highlight any discrepancies between the two solutions.
5. Incorporate insights from the edge case analysis.
6. Suggest which solution seems more accurate and why, considering the edge cases.

Provide your breakdown below:
"""

ENSEMBLE_PROMPT = """
Compare and analyze the given solutions, breakdown, edge case analysis, and validation results for the problem. Determine the most accurate solution and provide a final, correct answer with explanation.

1. Review all provided information: original solutions, edge case analysis, breakdown, and validation results.
2. Identify any discrepancies or errors highlighted by the validation process or edge case analysis.
3. Determine which solution is most accurate based on the breakdown, edge case analysis, and validation.
4. If necessary, make corrections or adjustments to the solution, taking into account the edge cases.
5. Provide a final, verified answer with a clear explanation of your reasoning, addressing any special scenarios or edge cases.

Provide your analysis and final answer below:
"""

VERIFY_PROMPT = """
Verify the ensemble solution for the given problem, taking into account the validation results and edge case analysis. Double-check all calculations and reasoning. If any errors are found, provide a corrected solution with explanations.

1. Carefully read the original problem, ensemble solution, validation results, and edge case analysis.
2. Verify each step of the solution, including all calculations and logical reasoning.
3. Check if the final answer makes sense in the context of the problem, aligns with the validation results, and addresses any edge cases.
4. If any errors are found, provide a detailed explanation and the correct solution.
5. If the solution is correct, confirm the final answer and provide a brief explanation of why it's correct, referencing the validation results and edge case analysis.

Provide your verification and final answer below:
"""

EXTRACT_ANSWER_PROMPT = """
Extract only the final numerical answer from the given solution. If there are multiple numbers, choose the one that represents the final answer to the problem. Do not include any units or additional text. Provide only the number as a decimal or integer.

For example, if the solution contains "The final answer is 20.00 hours", your response should be:
20.00

Extract and provide only the numerical answer below:
"""