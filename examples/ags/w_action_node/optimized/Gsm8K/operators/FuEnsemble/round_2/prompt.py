
FU_ENSEMBLE_PROMPT = """
### Given problem

{problem}

### We've got a list of solutions

<solutions>
{solutions}
</solutions>

### Instructions
Analyze the given problem and solution candidates to synthesize an improved, comprehensive solution:

1. Evaluate each solution:
   - Identify correct approaches and accurate calculations
   - Spot any errors or misconceptions
   - Assess the completeness and clarity of explanations

2. Synthesize the best elements:
   - Combine correct steps from different solutions
   - Fill gaps in reasoning or calculations
   - Ensure a logical flow from problem to solution

3. Enhance the integrated solution:
   - Provide clear, step-by-step reasoning
   - Include any necessary intermediate calculations
   - Explain key concepts or methods used
   - Address all aspects of the original problem

4. Final review:
   - Verify the accuracy of the synthesized solution
   - Ensure the solution is complete and addresses the entire problem
   - Check that the explanation is clear and easy to follow

Produce a single, cohesive solution that represents the best integration of all correct approaches while addressing any shortcomings in the individual solutions.
"""

