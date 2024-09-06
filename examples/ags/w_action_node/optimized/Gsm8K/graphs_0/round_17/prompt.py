GENERATE_PROMPT = """
Please follow these steps to solve the problem:

1. Break down the problem into smaller sub-problems if necessary.
2. For each sub-problem or the main problem if not broken down:
   a. Identify the relevant information and unknowns.
   b. Choose the appropriate mathematical concepts or formulas.
   c. Solve step by step, showing all your work.
3. Combine the solutions of sub-problems if applicable.
4. Verify your answer and ensure it makes sense in the context of the original problem.
5. Critically review your solution:
   a. Check for logical errors or inconsistencies.
   b. Ensure all steps are clearly explained.
   c. Verify that the final answer addresses the original question.

Now, please solve the problem step by step and include your self-review.
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
Please review the generated solution critically:

1. Check for logical errors or inconsistencies in the problem-solving process.
2. Ensure that all steps are clearly explained and justified.
3. Verify that the final answer directly addresses the original question.
4. Identify any potential improvements or alternative approaches.

Provide a brief review summary, highlighting any issues found or confirming the solution's validity.
"""