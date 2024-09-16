
FU_ENSEMBLE_PROMPT = """
### Given problem

{problem}

### We've got a list of solutions

<solutions>
{solutions}
</solutions>

### Instructions
Analyze the given problem and solution candidates to create an optimal, integrated solution:

1. Evaluate each solution's strengths and weaknesses.
2. Identify key concepts and correct approaches from different solutions.
3. Combine the best elements to form a comprehensive solution.
4. Ensure the integrated solution addresses all aspects of the problem.
5. Verify the mathematical correctness and logical flow of the final solution.
6. If applicable, suggest any additional insights or alternative methods not present in the original solutions.

Synthesize these findings into a clear, concise, and mathematically sound solution that surpasses the individual candidates in effectiveness and completeness.
"""

