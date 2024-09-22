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

VERIFY_INITIAL_SOLUTIONS_PROMPT = """
Review and verify the two initial solutions provided for the given problem. Check for any calculation errors, misinterpretations, or oversights. If errors are found, provide corrections and explanations.

1. Carefully read the original problem and both solutions.
2. Check each step of both solutions for accuracy in calculations and reasoning.
3. Identify any discrepancies between the two solutions.
4. If errors are found, provide detailed explanations and corrections.
5. If both solutions are correct but differ, explain why both approaches are valid.
6. Summarize your findings, including any corrections or confirmations of the solutions.

Provide your verification and analysis below:
"""

BREAKDOWN_PROMPT = """
Break down the given problem, solutions, and verification into clear, concise steps. Identify the key components of the problem and the mathematical operations used in each solution. Provide a structured analysis that can be easily validated programmatically.

1. Identify the important variables and values in the problem.
2. List the mathematical operations used in each solution.
3. Break down each solution into individual calculation steps.
4. Highlight any discrepancies between the two solutions and the verification results.
5. Suggest which solution seems more accurate and why, considering the verification.

Provide your breakdown below:
"""

ENSEMBLE_PROMPT = """
Compare and analyze the given solutions, breakdown, and validation results for the problem. Determine the most accurate solution and provide a final, correct answer with explanation.

1. Review all provided information: original solutions, verification, breakdown, and validation results.
2. Identify any discrepancies or errors highlighted by the verification and validation processes.
3. Determine which solution is most accurate based on the breakdown, verification, and validation.
4. If necessary, make corrections or adjustments to the solution.
5. Provide a final, verified answer with a clear explanation of your reasoning.

Provide your analysis and final answer below:
"""

VERIFY_PROMPT = """
Verify the ensemble solution for the given problem, taking into account the validation results. Double-check all calculations and reasoning. If any errors are found, provide a corrected solution with explanations.

1. Carefully read the original problem, ensemble solution, and validation results.
2. Verify each step of the solution, including all calculations and logical reasoning.
3. Check if the final answer makes sense in the context of the problem and aligns with the validation results.
4. If any errors are found, provide a detailed explanation and the correct solution.
5. If the solution is correct, confirm the final answer and provide a brief explanation of why it's correct, referencing the validation results.

Provide your verification and final answer below:
"""

EXTRACT_ANSWER_PROMPT = """
Extract only the final numerical answer from the given solution. If there are multiple numbers, choose the one that represents the final answer to the problem. Do not include any units or additional text. Provide only the number as a decimal or integer.

For example, if the solution contains "The final answer is 20.00 hours", your response should be:
20.00

Extract and provide only the numerical answer below:
"""