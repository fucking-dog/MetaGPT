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

REVIEW_PROMPT = """
Please review the generated solution for accuracy and completeness. Check for:
1. Correct application of mathematical concepts and formulas
2. Logical flow of steps
3. Completeness of the solution
4. Correct final answer

If any issues are found, please provide specific feedback for improvement.
"""

SELF_QUESTION_PROMPT = """
Before solving the problem, ask yourself the following questions:
1. What are the key components of this problem?
2. Are there any hidden assumptions or constraints?
3. What mathematical concepts or formulas are relevant to this problem?
4. Are there any special cases or edge conditions to consider?
5. What potential difficulties might arise in solving this problem?

Please provide brief answers to these questions.
"""