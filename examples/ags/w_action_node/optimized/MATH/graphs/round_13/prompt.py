DETAILED_SOLUTION_PROMPT = """
Please provide a detailed step-by-step solution for the given mathematical problem. Follow these guidelines:

1. State the problem clearly.
2. List all given information and identify what needs to be found.
3. Outline the approach and any relevant formulas or concepts.
4. Show all calculations in detail, using LaTeX notation for mathematical expressions.
5. Explain each step of your reasoning.
6. Interpret the code output (if provided) and incorporate it into your explanation.
7. Present the final answer, enclosing it in \boxed{} LaTeX notation.
8. Ensure all mathematical notation is in LaTeX format.

Your solution should be comprehensive, mathematically rigorous, and easy to follow.
"""

REFINE_ANSWER_PROMPT = """
Given the detailed solution, please refine and format the answer. Follow these guidelines:

1. Summarize the key steps of the solution process.
2. Ensure all mathematical expressions are in correct LaTeX notation.
3. Present the final answer clearly, enclosed in \boxed{} LaTeX notation.
4. If there are multiple possible answers, list all of them separated by commas within the \boxed{}.
5. Check for any logical inconsistencies or calculation errors.
6. Simplify expressions where possible without losing accuracy.

Your refined answer should be concise yet complete, mathematically accurate, and well-formatted.
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