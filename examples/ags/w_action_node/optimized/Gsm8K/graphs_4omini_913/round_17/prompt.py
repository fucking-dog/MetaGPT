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

SELF_REFLECT_PROMPT = """Given the problem and the refined solution, your task is to critically evaluate and potentially improve the solution through self-reflection. Follow these steps:

1. Carefully review the problem statement and the refined solution.
2. Assess the solution's correctness, completeness, and clarity.
3. Consider alternative approaches or methods that could lead to a more elegant or efficient solution.
4. Reflect on any assumptions made and verify their validity.
5. Identify any areas where the explanation could be enhanced or clarified.
6. If improvements are identified, incorporate them into the solution.
7. If the solution is already optimal, provide a brief explanation of why it is the best approach.

Provide the final solution, either improved or original, with a clear explanation of your self-reflection process and any changes made."""