DETAILED_SOLUTION_PROMPT = """
Given the mathematical problem and the output from the code execution, please provide a comprehensive and detailed step-by-step solution. Follow these guidelines:

1. Begin with a clear statement of the problem.
2. Explain the approach and any formulas or concepts used.
3. Show step-by-step calculations, using LaTeX notation for mathematical expressions.
4. Interpret the code output and incorporate it into your explanation.
5. Provide intermediate results and explanations for each step.
6. Ensure all mathematical notation is in LaTeX format.
7. Conclude with a final answer, enclosed in \boxed{} LaTeX notation.

Your response should be thorough, mathematically rigorous, and easy to follow, suitable for a student learning the concept.
"""

REVIEW_AND_REFINE_PROMPT = """
Please review and refine the given detailed solution for the mathematical problem. Follow these guidelines:

1. Check for mathematical accuracy and correctness.
2. Ensure all steps are logically connected and well-explained.
3. Verify that all LaTeX notation is correctly used and formatted.
4. Add any missing steps or explanations that could improve clarity.
5. Simplify overly complex explanations if possible.
6. Ensure the final answer is correct and properly enclosed in \boxed{} LaTeX notation.
7. If any errors are found, correct them and explain the correction.

Provide the refined solution, maintaining the step-by-step format and mathematical rigor of the original.
"""

GENERATE_SOLUTION_PROMPT = """
Please solve the given mathematical problem step by step. Follow these guidelines:

1. State the problem clearly.
2. Outline the approach and any relevant formulas or concepts.
3. Provide detailed calculations, using LaTeX notation for mathematical expressions.
4. Explain each step of your reasoning.
5. Present the final answer enclosed in \boxed{} LaTeX notation.
6. Ensure all mathematical notation is in LaTeX format.

Your solution should be thorough, mathematically sound, and easy to understand.
"""