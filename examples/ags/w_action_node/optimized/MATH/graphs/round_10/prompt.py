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
Please solve the given mathematical problem step by step. Follow these guidelines:

1. State the problem clearly.
2. Outline the approach and any relevant formulas or concepts.
3. Provide detailed calculations, using LaTeX notation for mathematical expressions.
4. Explain each step of your reasoning.
5. Present the final answer enclosed in \boxed{} LaTeX notation.
6. Ensure all mathematical notation is in LaTeX format.

Your solution should be thorough, mathematically sound, and easy to understand.
"""

STEP_BY_STEP_PROMPT = """
Provide a detailed, step-by-step solution to the given mathematical problem. Follow these guidelines:

1. Clearly state the problem and identify the key information given.
2. Break down the solution into logical steps, numbering each step.
3. For each step:
   a. Explain the reasoning behind the step.
   b. Show any calculations or transformations, using LaTeX notation for mathematical expressions.
   c. Provide intermediate results.
4. Use appropriate mathematical notation, formulas, and theorems, explaining them when first introduced.
5. Include visual aids (e.g., diagrams, graphs) if they help clarify the solution, describing them in LaTeX format.
6. Conclude with the final answer, enclosed in \boxed{} LaTeX notation.
7. Add a brief explanation of the significance of the result or any important observations.

Ensure your solution is clear, concise, and mathematically rigorous, suitable for a student learning the concept.
"""