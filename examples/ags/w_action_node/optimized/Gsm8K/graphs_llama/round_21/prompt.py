ALTERNATIVE_APPROACH_PROMPT = """
You are a creative problem solver. Given a math problem, your task is to propose an alternative approach to solve it. This approach should be different from the most obvious or common method. Consider using unconventional techniques, different mathematical concepts, or innovative problem-solving strategies. Provide a step-by-step solution using this alternative approach.

Problem: {input}

Please provide your alternative solution approach:
"""

FINAL_SOLUTION_PROMPT = """
You are an expert mathematician tasked with providing a clear and concise final solution to a math problem. Review the given problem and the proposed solution, then create a well-structured, step-by-step explanation of the solution. Ensure that your explanation is easy to understand, logically organized, and mathematically accurate. Include any necessary calculations, proofs, or reasoning steps.

{input}

Please provide the final, refined solution:
"""