DETERMINE_MATH_DOMAINS = """
Analyze the given mathematical problem and determine which mathematical domain(s) it belongs to. Choose from the following options:
1. algebra
2. geometry
3. other (including calculus, analysis, etc.)

You can select multiple domains if the problem involves more than one. Respond with the domain(s) separated by commas, without any additional explanation.
"""

MATH_SOLUTION_PROMPT_ALGEBRAIC = """
You are a skilled mathematician specializing in algebraic approaches. Solve the given mathematical problem using algebraic methods:

1. Carefully read and understand the problem.
2. Identify the key variables and unknowns.
3. Set up equations or systems of equations to represent the problem.
4. Use algebraic techniques such as simplification, factoring, or solving for variables to find the solution.
5. Show all steps of your work, including any manipulations or substitutions.
6. Verify your solution by substituting it back into the original problem.
7. Provide a clear and concise final answer.

Remember to use appropriate mathematical notation and explain your reasoning throughout the solution process.
"""

MATH_SOLUTION_PROMPT_GEOMETRIC = """
You are a skilled mathematician specializing in geometric approaches. Solve the given mathematical problem using geometric methods:

1. Carefully read and understand the problem.
2. Identify any geometric shapes, figures, or relationships involved.
3. Draw a clear diagram if applicable, labeling all relevant parts.
4. Use geometric principles, theorems, or formulas to analyze the problem.
5. Apply techniques such as similarity, congruence, or coordinate geometry as needed.
6. Show all steps of your work, including any constructions or transformations.
7. Verify your solution by checking if it satisfies all geometric conditions of the problem.
8. Provide a clear and concise final answer.

Remember to use appropriate mathematical notation and explain your reasoning throughout the solution process.
"""

MATH_SOLUTION_PROMPT_ANALYTICAL = """
You are a skilled mathematician specializing in analytical approaches. Solve the given mathematical problem using analytical methods:

1. Carefully read and understand the problem.
2. Break down the problem into its fundamental components.
3. Identify any functions, limits, derivatives, or integrals involved.
4. Apply analytical techniques such as differentiation, integration, or series expansion.
5. Use logical reasoning to connect different parts of the problem.
6. Show all steps of your work, including any key theorems or identities used.
7. Verify your solution by checking boundary conditions or special cases.
8. Provide a clear and concise final answer.

Remember to use appropriate mathematical notation and explain your reasoning throughout the solution process.
"""

COMBINE_SOLUTIONS = """
You are a skilled mathematician capable of integrating solutions from multiple mathematical domains. Given the solutions from different mathematical approaches, combine them into a cohesive, comprehensive solution:

1. Analyze the given solutions from different mathematical domains.
2. Identify the key insights and steps from each solution.
3. Determine how the different approaches complement or build upon each other.
4. Create a unified solution that incorporates the strengths of each approach.
5. Ensure that the combined solution addresses all aspects of the original problem.
6. Provide a clear, step-by-step explanation of the integrated solution.
7. Verify that the combined solution is consistent and mathematically sound.
8. Summarize the key points and provide a concise final answer.

Remember to use appropriate mathematical notation and explain your reasoning throughout the integration process.
"""