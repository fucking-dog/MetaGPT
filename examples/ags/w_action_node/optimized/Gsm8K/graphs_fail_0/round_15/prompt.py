COMPLEXITY_ANALYSIS_PROMPT = """
Analyze the given mathematical problem and determine its complexity level. Categorize it as one of the following:
1. Simple: Basic arithmetic, single-step problems, or straightforward applications of fundamental concepts.
2. Moderate: Multi-step problems, basic algebra, geometry, or problems requiring some logical reasoning.
3. Complex: Advanced algebra, calculus, multi-variable problems, or those requiring sophisticated problem-solving techniques.

Provide your assessment as a single word: 'simple', 'moderate', or 'complex'.
"""

MATH_SOLUTION_PROMPT_SIMPLE = """
Solve the given simple mathematical problem:

1. Read and understand the problem carefully.
2. Identify the key information and what needs to be calculated.
3. Choose the appropriate basic mathematical operation(s) needed (addition, subtraction, multiplication, division).
4. Perform the calculation step-by-step, showing your work clearly.
5. Double-check your calculation for accuracy.
6. Present the final answer clearly, including appropriate units if applicable.

Remember to use clear and concise language in your explanation.
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