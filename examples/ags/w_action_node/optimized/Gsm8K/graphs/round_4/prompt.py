GENERATE_PROMPT = """
Generate Solution for the following problem: {input}
"""

REPHRASE_PROMPT = """
{input}
### Instructions
When faced with this math problem, your goal is to:

1. Extract the core question: Carefully read the problem and distill it into a single, comprehensive sentence that captures the essence of what is being asked.

2. Restate the problem in your own words: Understand the basic requirements and conditions, then rephrase the problem, making sure to include all nuances, details, notes, and examples provided in the original problem description.

3. List the key points for solving the problem: Identify and list the known conditions, unknowns, and any relevant mathematical concepts or formulas that will be necessary to apply in order to solve the problem.

4. Consider possible strategies and methods: Think about various approaches to breaking down the problem into manageable parts or steps.

5. Represent the problem mathematically: Use mathematical expressions or equations to represent the problem, preparing for the solution process.

6. Analyze the question: Provide an analysis of the question without giving away the answer.
"""

VALIDATE_PROMPT = """
Please review and validate the following solution:

{input}

Instructions:
1. Check if the solution addresses all parts of the original problem.
2. Verify the mathematical accuracy of the solution.
3. Ensure the solution's logic is sound and well-explained.
4. Identify any potential errors or areas for improvement.
5. If the solution is correct and complete, state "The solution is valid."
6. If the solution needs improvement, provide specific feedback on what needs to be corrected or added.
"""

SELF_REFLECT_PROMPT = """
Critically evaluate the following solution:

{input}

Instructions:
1. Analyze the solution step by step.
2. Check for any logical errors or missed steps.
3. Ensure all parts of the problem are addressed.
4. Consider alternative approaches or simplifications.
5. Suggest improvements or corrections if necessary.
6. If the solution seems correct and complete, state "The solution appears sound."
"""

CALCULATE_PROMPT = """
Analyze the following problem and solution:

{input}

If the problem requires numerical calculations:
1. Identify the mathematical expression that needs to be evaluated.
2. Format this expression so it can be safely evaluated using Python's eval() function.
3. Provide the formatted expression as the output.

If no numerical calculation is required, simply state "No calculation needed."
"""