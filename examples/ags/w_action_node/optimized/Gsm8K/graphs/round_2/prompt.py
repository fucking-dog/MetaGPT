GENERATE_PROMPT = """
To solve the given problem, follow these steps:
1. Break down the problem into smaller, manageable parts.
2. For each part:
   a. Identify the key information and unknowns.
   b. Determine the appropriate mathematical operations or formulas to use.
   c. Perform the calculations step by step.
3. Combine the results from each part to form the final solution.
4. Review your answer to ensure it makes sense in the context of the original problem.

Problem: {problem_description}

Provide a detailed solution following the steps above.
"""

ANSWER_FORMAT_PROMPT = """
[Your solution here]
"""