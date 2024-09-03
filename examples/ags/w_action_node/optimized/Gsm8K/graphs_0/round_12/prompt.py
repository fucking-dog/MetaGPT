GENERATE_PROMPT = """
Please reason step by step, and solve the problem.
"""

REPHRASE_PROMPT = """
### Instructions
When faced with this math problem, your goal is to:

1. Extract the core question: Carefully read the problem and distill it into a single, comprehensive sentence that captures the essence of what is being asked.

2. Restate the problem in your own words: Understand the basic requirements and conditions, then rephrase the problem, making sure to include all nuances, details, notes, and examples provided in the original problem description.

3. List the key points for solving the problem: Identify and list the known conditions, unknowns, and any relevant mathematical concepts or formulas that will be necessary to apply in order to solve the problem.

4. Consider possible strategies and methods: Think about various approaches to breaking down the problem into manageable parts or steps.

5. Represent the problem mathematically: Use mathematical expressions or equations to represent the problem, preparing for the solution process.

6. Analyze the question: Provide an analysis of the question without giving away the answer.
"""

REVIEW_PROMPT = """
Please review the generated solution for accuracy and completeness. Check for:
1. Correct application of mathematical concepts and formulas
2. Logical flow of steps
3. Completeness of the solution
4. Correct final answer

If any issues are found, please provide specific feedback for improvement.
"""

SELF_QUESTION_PROMPT = """
Now that you have generated a solution, please ask yourself the following questions:
1. Are there any alternative approaches to solving this problem?
2. Have I considered all possible edge cases or special scenarios?
3. Is there a more efficient way to solve this problem?
4. Are there any assumptions I've made that might not always hold true?
5. How can I verify the correctness of my solution?

Based on your answers to these questions, revise your solution if necessary.
"""

NUMERICAL_CHECK_PROMPT = """
Please perform a numerical accuracy check on the solution:
1. Verify all calculations are correct
2. Check for any rounding errors
3. Ensure all units are consistent and correct
4. Confirm that the final answer makes sense in the context of the problem

If any numerical issues are found, please provide specific feedback for correction.
"""