REFINE_ANSWER_PROMPT = """
Given the mathematical problem and the output from the code execution, please provide a well-formatted and detailed solution. Follow these guidelines:

1. Begin with a clear statement of the problem.
2. Explain the approach and any formulas or concepts used.
3. Show step-by-step calculations, using LaTeX notation for mathematical expressions.
4. Interpret the code output and incorporate it into your explanation.
5. Provide a final answer, enclosed in \boxed{} LaTeX notation.
6. Ensure all mathematical notation is in LaTeX format.

Your response should be comprehensive, mathematically rigorous, and easy to follow.
"""

GENERATE_SOLUTION_PROMPT = """
Please solve the given mathematical problem following these guidelines:

1. State the problem clearly.
2. Outline your approach and any relevant formulas or concepts.
3. Provide a step-by-step solution, using LaTeX notation for mathematical expressions.
4. Include a final answer enclosed in \boxed{} LaTeX notation.
5. Ensure all mathematical notation is in LaTeX format.

Your solution should be clear, concise, and mathematically sound.
"""