
FU_ENSEMBLE_PROMPT = """
### Given problem

{problem}

### We've got a list of solutions

<solutions>
{solutions}
</solutions>

### Instructions
Analyze the given problem and solution candidates to synthesize an optimal, comprehensive solution:

1. Evaluate each solution:
   - Identify correct approaches, accurate calculations, and valid reasoning
   - Detect any errors, misconceptions, or logical flaws
   - Assess completeness, clarity, and efficiency of explanations

2. Synthesize the best elements:
   - Integrate correct steps and methodologies from different solutions
   - Address gaps in reasoning, calculations, or problem-solving approaches
   - Ensure a coherent, logical progression from problem statement to final answer

3. Enhance the integrated solution:
   - Provide a clear, step-by-step solution with concise explanations
   - Include all necessary intermediate calculations and key reasoning steps
   - Explain fundamental concepts or methods crucial to problem-solving
   - Ensure all aspects of the original problem are thoroughly addressed

4. Optimize and refine:
   - Streamline the solution for clarity and efficiency
   - Eliminate redundancies while maintaining comprehensiveness
   - Highlight key insights or innovative approaches from the original solutions

5. Final review:
   - Verify the mathematical accuracy and logical consistency of the synthesized solution
   - Confirm the solution fully resolves all components of the problem
   - Ensure the explanation is accessible, precise, and well-structured

Produce a single, cohesive solution that represents the most effective integration of all correct approaches, addresses any shortcomings in the individual solutions, and presents the clearest path to problem resolution.
"""

