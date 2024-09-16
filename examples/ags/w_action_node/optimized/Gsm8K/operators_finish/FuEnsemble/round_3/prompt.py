
FU_ENSEMBLE_PROMPT = """
### Given problem

{problem}

### We've got a list of solutions

<solutions>
{solutions}
</solutions>

### Instructions
Analyze the given problem and solution candidates to create an optimal, integrated solution:

1. Evaluate each solution's approach, accuracy, and completeness
2. Identify unique strategies, insights, or efficient methods from different solutions
3. Combine the most effective elements to form a comprehensive solution
4. Ensure the integrated solution addresses all aspects of the problem and any potential edge cases
5. Verify the mathematical accuracy, logical consistency, and efficiency of the final solution
6. If applicable, suggest any optimizations or alternative approaches that could further improve the solution

Synthesize these findings into a clear, concise, and mathematically rigorous solution that:
- Incorporates the best aspects of all candidate solutions
- Provides a step-by-step explanation that's easy to follow
- Uses the most efficient methods identified
- Addresses any limitations or assumptions in the original solutions
- Demonstrates a deep understanding of the underlying mathematical principles

Your final integrated solution should be significantly more robust, accurate, and insightful than any individual candidate solution.
"""

