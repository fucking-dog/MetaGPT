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

DETAILED_SOLUTION_PROMPT = """
Provide a comprehensive, step-by-step solution to the given mathematical problem. Your response should include:

1. A clear restatement of the problem.
2. An explanation of the mathematical concepts and formulas involved.
3. A detailed, logical progression of steps to solve the problem.
4. Clear explanations for each step, including the reasoning behind it.
5. All mathematical expressions and equations in LaTeX format.
6. Visual aids or diagrams if applicable (described in text).
7. A final answer clearly marked and enclosed in \boxed{} LaTeX notation.
8. A brief explanation of the significance of the answer in the context of the original problem.

Aim for clarity, accuracy, and thoroughness in your solution.
"""

EXPLANATION_SOLUTION_PROMPT = """
Provide a solution to the given mathematical problem with a focus on explanations and understanding. Your response should include:

1. A clear restatement of the problem.
2. An in-depth explanation of the key mathematical concepts and principles involved.
3. A step-by-step solution, emphasizing the reasoning behind each step.
4. Clarification of any potential misconceptions or common errors related to the problem.
5. All mathematical expressions and equations in LaTeX format.
6. Analogies or real-world examples to illustrate the concepts, if applicable.
7. A final answer clearly marked and enclosed in \boxed{} LaTeX notation.
8. A discussion on how this problem relates to broader mathematical topics or applications.

Your goal is to not only solve the problem but also to enhance the reader's understanding of the underlying mathematical principles.
"""