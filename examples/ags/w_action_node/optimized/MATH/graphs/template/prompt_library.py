PROBLEM_BREAKDOWN_PROMPT = """ Break down the given mathematical problem into smaller, manageable steps. Identify the key components, variables, and relationships within the problem. List these elements clearly and explain how they interact or relate to each other. This breakdown should serve as a roadmap for solving the problem systematically. """
THEOREM_IDENTIFICATION_PROMPT = """ Analyze the problem and identify any relevant mathematical theorems, formulas, or principles that may be applicable. Explain why each identified theorem or principle is relevant to the problem at hand. If multiple approaches are possible, list them in order of potential effectiveness or simplicity. """
STEP_BY_STEP_SOLUTION_PROMPT = """ Provide a detailed, step-by-step solution to the mathematical problem. For each step:
Clearly state the action being taken.
Explain the reasoning behind the step.
Show all calculations or transformations in detail.
Highlight any key decisions or assumptions made during the process. Ensure that each step logically follows from the previous one and leads towards the final solution. """
VARIABLE_DEFINITION_PROMPT = """ Clearly define all variables, constants, and parameters used in the problem and solution. For each:
Provide its mathematical symbol or notation.
Explain its meaning or what it represents in the context of the problem.
Specify its units of measurement, if applicable.
Note any constraints or limitations on its values. This definition set should serve as a comprehensive reference throughout the solution process. """
EQUATION_FORMULATION_PROMPT = """ Formulate the mathematical equations necessary to solve the problem. For each equation:
Write it in standard mathematical notation.
Explain what the equation represents or models in the context of the problem.
Justify why this particular equation is relevant or necessary for the solution.
If the equation is derived from a more general form, show the derivation process. """
MATHEMATICAL_PROOF_PROMPT = """ Construct a rigorous mathematical proof for the solution or a key component of the problem. Follow these guidelines:
State the theorem or claim to be proved.
List all assumptions and given information.
Proceed logically, step by step, using valid mathematical reasoning.
Justify each step with references to definitions, axioms, or previously proven results.
Clearly indicate the conclusion of the proof. Ensure that the proof is complete, leaving no logical gaps. """
ERROR_ANALYSIS_PROMPT = """ Perform a comprehensive error analysis on the solution. This should include:
Identifying potential sources of error in the problem-solving process.
Estimating the magnitude of these errors and their impact on the final result.
Discussing any approximations or simplifications made and their justification.
Suggesting methods to minimize or account for these errors in future calculations.
If applicable, providing error bounds or confidence intervals for the solution. """
ALGEBRAIC_MANIPULATION_PROMPT = """ Perform detailed algebraic manipulations to simplify expressions, solve equations, or transform the problem into a more manageable form. For each manipulation:
Clearly state the operation being performed (e.g., factoring, expanding, substituting).
Show each intermediate step of the manipulation.
Explain the reasoning behind choosing this particular manipulation.
Verify that the manipulation preserves the mathematical equivalence of the expressions. """
NUMERICAL_METHOD_APPLICATION_PROMPT = """ Apply appropriate numerical methods to solve or approximate the solution to the problem. This should include:
Selecting a suitable numerical method (e.g., Newton's method, Runge-Kutta, Monte Carlo).
Explaining why this method is appropriate for the given problem.
Detailing the algorithm or process of the chosen method.
Implementing the method step-by-step, showing all calculations.
Discussing the convergence, accuracy, and efficiency of the method.
Providing error estimates or bounds for the numerical solution. """
MATHEMATICAL_MODELING_PROMPT = """ Develop a mathematical model to represent the problem or system described. This process should include:
Identifying the key variables and parameters of the system.
Formulating equations or inequalities that describe the relationships between these variables.
Stating any assumptions or simplifications made in creating the model.
Explaining how each component of the model corresponds to real-world elements of the problem.
Discussing the limitations and scope of applicability of the model.
If possible, suggesting methods to validate or test the model's accuracy. """