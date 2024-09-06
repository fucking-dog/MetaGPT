MATH_PROBLEM_SOLVING = """
Given a mathematical problem, follow these steps to solve it:

1. Carefully read and understand the problem statement.
2. Identify the key information and unknowns.
3. Determine the appropriate mathematical concepts or formulas needed.
4. Plan your solution approach step by step.
5. Execute the plan, showing all your work clearly.
6. Check your solution for correctness and reasonableness.
7. Provide a clear, concise final answer.

Please solve the given problem following these steps.
"""

MATH_PROBLEM_REVISION = """
Given a mathematical problem, its previous solution, and feedback on that solution, please revise the solution. Follow these steps:

1. Carefully review the original problem statement.
2. Analyze the previous solution and the provided feedback.
3. Identify the areas that need improvement or correction.
4. Develop a revised solution that addresses the feedback and corrects any errors.
5. Ensure that your revised solution is complete, clear, and accurate.
6. Double-check your work for any new errors or inconsistencies.
7. Provide the revised solution, showing all steps clearly.

Please revise the solution based on the given information and feedback.
"""

METHOD_CHECK = """
Analyze the given mathematical problem and determine if it requires multiple solution methods (e.g., algebraic, geometric, and numerical approaches) for a comprehensive solution. 

Respond with 'Yes' if multiple methods would provide valuable insights or a more robust solution.
Respond with 'No' if a single, straightforward method is sufficient.

Base your decision on the problem's complexity, potential for different perspectives, and the benefits of applying various mathematical techniques.
"""

MULTI_METHOD_SOLVING = """
Given a mathematical problem, solve it using the {method} approach. Follow these steps:

1. Carefully read and understand the problem statement.
2. Identify the key information and unknowns relevant to the {method} approach.
3. Determine the appropriate {method} concepts, formulas, or techniques needed.
4. Plan your solution approach step by step using {method} methods.
5. Execute the plan, showing all your work clearly.
6. Check your solution for correctness and reasonableness within the context of the {method} approach.
7. Provide a clear, concise final answer, emphasizing the insights gained from the {method} perspective.

Please solve the given problem following these steps, focusing on the {method} method.
"""