GENERATE_PROMPT = """
Please follow these steps to solve the problem:
1. Simplify the problem: Break down the complex problem into smaller, more manageable parts if necessary.
2. Reason step by step: Provide a clear, logical progression of your thought process.
3. Solve the problem: Apply appropriate mathematical concepts and formulas to reach the solution.
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