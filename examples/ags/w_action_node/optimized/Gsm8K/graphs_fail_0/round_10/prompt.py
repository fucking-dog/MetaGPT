ANALYZE_MATH_PROBLEM = """
Analyze the given mathematical problem and determine which mathematical domain(s) it belongs to. Choose from the following options:
1. algebra
2. geometry
3. other (including calculus, analysis, etc.)

If the problem requires multiple steps or approaches from different domains, list all relevant domains separated by commas.
Respond with only the domain(s) without any additional explanation.
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
You are given multiple solution steps for a complex mathematical problem that requires approaches from different mathematical domains. Your task is to combine these solutions into a coherent, step-by-step solution that addresses all aspects of the problem. Follow these guidelines:

1. Analyze the given solution steps and identify their logical order.
2. Combine the steps into a single, comprehensive solution.
3. Ensure smooth transitions between different mathematical domains.
4. Maintain consistency in notation and terminology throughout the combined solution.
5. Verify that all parts of the original problem are addressed in the final solution.
6. Provide clear explanations for each step, especially when transitioning between different mathematical approaches.
7. Include a final answer or conclusion that encompasses all aspects of the problem.

Present the combined solution in a clear, logical, and easy-to-follow format.
"""