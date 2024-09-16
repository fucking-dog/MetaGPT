REFINE_PROMPT = """Given the problem and the proposed solution, your task is to refine and improve the solution. Follow these steps:

1. Analyze the problem statement carefully.
2. Review the proposed solution for correctness and completeness.
3. Identify any potential improvements in clarity, efficiency, or mathematical rigor.
4. Refine the solution by:
   - Correcting any errors or inconsistencies
   - Enhancing the explanation where needed
   - Simplifying steps if possible
   - Ensuring all parts of the problem are addressed
5. Provide the refined solution with clear, step-by-step reasoning.

Remember to maintain mathematical accuracy and provide a solution that is both correct and easy to understand."""

MULTI_APPROACH_PROMPT = """Given the problem and a specified approach, generate a solution using that approach. Follow these steps:

1. Analyze the problem statement carefully.
2. Consider the specified approach (algebraic, geometric, or numerical).
3. Develop a solution strategy using the given approach.
4. Provide a clear, step-by-step solution using the specified approach.
5. Ensure that your solution is mathematically accurate and addresses all parts of the problem.

Remember to tailor your solution to the given approach while maintaining clarity and correctness."""