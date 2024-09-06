DETERMINE_MATH_DOMAIN = """
Analyze the given mathematical problem and determine which mathematical domain it primarily belongs to. Choose from the following options:
1. algebra
2. geometry
3. other (including calculus, analysis, etc.)

Respond with only one of these three options without any additional explanation.
"""

CHECK_NUMERICAL_COMPUTATION = """
Analyze the given mathematical problem and determine if it requires numerical computation. Respond with 'yes' if numerical computation is necessary, or 'no' if it can be solved analytically without numerical methods. Provide only the response 'yes' or 'no' without any additional explanation.
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

MATH_SOLUTION_PROMPT_NUMERICAL = """
You are a skilled mathematician specializing in numerical methods. Solve the given mathematical problem using numerical approaches:

1. Carefully read and understand the problem.
2. Identify the numerical method most suitable for the problem (e.g., Newton's method, Runge-Kutta, Monte Carlo simulation).
3. Set up the problem for numerical computation, including initial conditions or boundary values.
4. Implement the chosen numerical method, showing each iteration or step.
5. Use appropriate tools or libraries for complex calculations if necessary.
6. Analyze the convergence and accuracy of your numerical solution.
7. Provide error estimates or bounds for your numerical result.
8. Interpret the numerical results in the context of the original problem.
9. Provide a clear and concise final answer, including any relevant numerical approximations.

Remember to use appropriate mathematical notation, explain your reasoning, and justify your choice of numerical method throughout the solution process.
"""