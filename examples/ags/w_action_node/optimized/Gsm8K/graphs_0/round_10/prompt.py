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

SELF_EVALUATE_PROMPT = """
Please evaluate the quality and completeness of the solution you've provided. Consider the following:

1. Does the solution address all aspects of the problem?
2. Are the steps clearly explained and logically connected?
3. Is the mathematical reasoning sound?
4. Are there any potential errors or oversights?
5. Is the solution presented in a clear and organized manner?

If you identify any issues or areas for improvement, please revise the solution accordingly.
"""