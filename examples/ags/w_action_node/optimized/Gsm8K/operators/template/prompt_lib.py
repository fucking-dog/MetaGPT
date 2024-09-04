READ_PROBLEM_CAREFULLY_PROMPT = """Carefully read the problem, ensuring complete understanding of all given information and requirements:
- Read through the entire problem statement multiple times, not missing any details.
- Identify and mark all known conditions, variables, and constants.
- Clearly understand what the problem asks you to find or prove.
- Pay attention to any special constraints or assumptions.
- Rephrase the problem in your own words to confirm understanding.
- Identify the mathematical fields involved (e.g., algebra, geometry, calculus).
- Consider if additional background knowledge is needed to understand the problem."""

VISUALIZE_PROBLEM_PROMPT = """Draw relevant diagrams or sketches to visualize the relationships and conditions in the problem:
- For geometric problems, draw precise figures, labeling all known angles, lengths, etc.
- For functional relationships, sketch function graphs, marking key points and intervals.
- Use Venn diagrams to represent set relationships.
- Draw tree diagrams or tables for probability problems.
- For physics problems, draw force analysis diagrams or motion trajectory graphs.
- Use flowcharts to represent algorithms or processes.
- Ensure the diagrams include all relevant information and are clearly labeled."""

DECOMPOSE_COMPLEX_PROBLEM_PROMPT = """Break down complex problems into several smaller sub-problems:
- Identify the main components or stages of the problem.
- Transform each part into an independent sub-problem.
- Determine the logical relationships and dependencies between sub-problems.
- Arrange sub-problems in order from simple to complex.
- Consider if some sub-problems can be solved in parallel.
- Establish specific solution goals for each sub-problem.
- Ensure that the solutions to all sub-problems can be combined into a complete problem solution."""

LIST_CONDITIONS_AND_MODEL_PROMPT = """List all known conditions and unknowns, and establish appropriate mathematical models or equations:
- Use clear symbols to represent each known and unknown quantity.
- Specify the units and possible value ranges for each variable.
- Write out all given equations or inequalities based on the problem description.
- Consider implicit conditions in the problem and translate them into mathematical expressions.
- Choose appropriate mathematical tools (e.g., equations, matrices, differential equations) to describe the problem.
- Check if the model completely captures all aspects of the problem.
- Ensure the number of equations in the model matches the number of unknowns."""

CONSIDER_MULTIPLE_STRATEGIES_PROMPT = """Consider multiple possible problem-solving strategies, weighing the pros and cons of each method:
- List all potentially applicable mathematical methods (e.g., algebraic, geometric, calculus-based approaches).
- Evaluate the complexity and feasibility of each method.
- Consider potential difficulties or pitfalls for each method.
- Judge which method is most likely to yield accurate and complete solutions.
- Consider if multiple methods can be combined to solve the problem.
- Assess the differences in computational efficiency between different methods.
- Choose the method best suited to the current problem and your personal expertise."""

DERIVE_SOLUTION_LOGICALLY_PROMPT = """Derive the solution step by step following rigorous mathematical logic:
- Start from known conditions and proceed step by step.
- Have clear mathematical basis (such as theorems, formulas, properties) for each step.
- Clearly state the purpose and reason for each step.
- Maintain consistency in symbols and expressions.
- Provide detailed explanations for key steps.
- Ensure logical coherence and completeness.
- Use mathematical symbols and terminology appropriately to increase precision of expression."""

CHECK_INTERMEDIATE_RESULTS_PROMPT = """Frequently check the reasonableness of intermediate results during the problem-solving process:
- Regularly review completed steps to ensure there are no logical jumps.
- Check if the order of magnitude of intermediate results is reasonable.
- Verify if intermediate results satisfy the known conditions of the problem.
- If contradictions or unreasonable results appear, carefully check previous steps.
- Consider special cases or limit situations to see if the results still hold.
- Use intuition or experience to judge if results meet expectations.
- If errors are found, systematically backtrack and correct, rather than just modifying the last step."""

UTILIZE_MATHEMATICAL_TOOLS_PROMPT = """Make good use of mathematical tools and theorems, such as calculus, linear algebra, probability theory, etc.:
- Choose the most suitable mathematical branch and tools based on the problem type.
- Correctly apply relevant theorems, formulas, and methods.
- Consider if the problem can be simplified through coordinate transformations or other techniques.
- Utilize computer algebra systems for complex calculations or symbolic operations.
- Use numerical methods or approximation techniques when appropriate.
- Flexibly apply knowledge from different mathematical branches to seek innovative solutions.
- Note the connections between different mathematical tools, applying them comprehensively to solve complex problems."""

VERIFY_FINAL_ANSWER_PROMPT = """Attempt to verify the correctness of the final answer using different methods:
- Substitute the result back into the original problem to check if it satisfies all conditions.
- Re-solve the problem using different solution methods and compare results.
- Consider special cases or boundary conditions of the problem to verify if the result still holds.
- Use mathematical software for numerical verification or graphical visualization.
- Check if the dimensions of the result are correct.
- Compare with known results of similar problems.
- If possible, consider the inverse process of the problem to see if the original conditions can be obtained."""

SUMMARIZE_SOLUTION_PROMPT = """Summarize the problem-solving process and results using clear and concise language:
- Review the main content and objectives of the problem.
- Summarize the main methods used and key steps.
- Clearly state the final result, including all relevant values, expressions, or conclusions.
- Explain the meaning and applicable range of the result.
- Point out any assumptions or limitations in the solution.
- If there are multiple solutions, clearly state all possible solutions and their conditions.
- Consider the practical application significance of the result, if applicable.
- Provide a brief discussion of the result, including its reasonableness and possible generalizations."""