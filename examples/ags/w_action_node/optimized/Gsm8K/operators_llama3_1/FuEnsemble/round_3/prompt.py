
FU_ENSEMBLE_PROMPT = """
### Given problem

{problem}

### We've got a list of solutions

<solutions>
{solutions}
</solutions>

### Instructions
Analyze the given problem and solution candidates to create an optimized, comprehensive solution:

1. Evaluation:
   - Identify the key aspects of the problem that need to be addressed
   - Assess each solution's strengths and weaknesses in relation to these aspects
   - Determine which solutions provide the most accurate and efficient approaches

2. Integration:
   - Select the best elements from each solution
   - Combine these elements logically, ensuring they complement each other
   - Address any gaps or inconsistencies in the integrated approach

3. Enhancement:
   - Refine the integrated solution for clarity and precision
   - Add any missing steps or explanations to make the solution more comprehensive
   - Ensure the final solution is mathematically sound and follows a clear, logical progression

4. Verification:
   - Double-check that the enhanced solution fully addresses all aspects of the original problem
   - Confirm that the solution is presented in a clear, step-by-step manner

Synthesize these insights into a final, optimized solution that surpasses the individual candidates in completeness, accuracy, and clarity.
"""

