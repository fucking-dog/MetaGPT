
GENERATE_PROMPT = """
Generate Solution for the following problem: 
{problem}
"""


CONTEXTUAL_GENERATE_PROMPT = """
Analyze and solve the given mathematical problem:

Problem:
{problem}

Key Information:
{context}

Approach:
1. Carefully examine the problem and the provided key information.
2. Identify the relevant mathematical concepts and formulas needed.
3. Break down the problem into smaller, manageable steps.
4. Solve each step methodically, showing your work clearly.
5. Double-check your calculations and reasoning.
6. Provide a clear, concise final answer.

Remember to use precise mathematical language and notation throughout your solution.
"""


REVIEW_PROMPT = """
As an expert reviewer, your task is to critically evaluate the given solution for the presented problem. Consider the following criteria:

1. Accuracy: Does the solution correctly address all aspects of the problem?
2. Completeness: Is every step of the problem-solving process accounted for?
3. Clarity: Is the solution explained in a logical and easy-to-follow manner?
4. Efficiency: If relevant, does the solution use an optimal approach?

Problem: {problem}

Proposed Solution: {solution}

Provide your assessment as follows:
1. A boolean value (True/False) indicating if the solution meets all criteria satisfactorily.
2. A concise explanation of your decision, highlighting strengths and/or areas needing improvement.

Focus solely on the solution's quality and correctness, disregarding formatting or presentation style.
"""


REVISE_PROMPT = """
Given the mathematical problem: {problem}

And the initial solution: {solution}

Considering the review feedback: {feedback}

Please follow these steps to revise the solution:
1. Analyze the initial solution and identify any errors or areas for improvement mentioned in the feedback.
2. Address each point of feedback systematically.
3. If necessary, provide additional steps or explanations to clarify the solution.
4. Ensure all calculations are accurate and clearly presented.
5. Summarize the key changes made to improve the solution.

Provide the revised, comprehensive solution that addresses all feedback and ensures mathematical accuracy.
"""


FU_ENSEMBLE_PROMPT = """
### Given problem

{problem}

### We've got a list of solutions

<solutions>
{solutions}
</solutions>

### Instructions
Analyze the given problem and solution candidates to create an optimized, comprehensive solution:

1. Evaluation:
   - Identify the key aspects of the problem that need to be addressed
   - Assess each solution's strengths and weaknesses in relation to these aspects
   - Determine which solutions provide the most accurate and efficient approaches

2. Integration:
   - Select the best elements from each solution
   - Combine these elements logically, ensuring they complement each other
   - Address any gaps or inconsistencies in the integrated approach

3. Enhancement:
   - Refine the integrated solution for clarity and precision
   - Add any missing steps or explanations to make the solution more comprehensive
   - Ensure the final solution is mathematically sound and follows a clear, logical progression

4. Verification:
   - Double-check that the enhanced solution fully addresses all aspects of the original problem
   - Confirm that the solution is presented in a clear, step-by-step manner

Synthesize these insights into a final, optimized solution that surpasses the individual candidates in completeness, accuracy, and clarity.
"""


MD_ENSEMBLE_PROMPT = """
Analyze the following problem:
{problem}

You have been provided with multiple candidate solutions:
{solutions}

Your task is to select the optimal solution for this problem. Consider the following criteria:
1. Correctness: The solution must fully address all aspects of the problem.
2. Robustness: The solution should handle various input scenarios and edge cases.
3. Efficiency: While not the primary factor, consider the solution's performance.
4. Readability: The code should be clear and well-structured.
5. Scalability: The solution should work for larger inputs if applicable.

Evaluate each solution against these criteria. If a solution fails to meet any of these criteria, it should not be selected.

Provide your final decision by writing only the chosen solution letter.
"""


SC_ENSEMBLE_PROMPT = """
You are an expert in evaluating mathematical solutions. Your task is to analyze multiple solutions to the following problem:

{problem}

Here are the proposed solutions:

{solutions}

Your objective is to:
1. Carefully examine each solution for correctness and logical consistency.
2. Identify the solution that appears most frequently or shares the most common elements with other solutions.
3. If there's a tie, select the solution with the most detailed and clear explanation.
4. Choose the solution that best aligns with established mathematical principles and problem-solving techniques.

Provide your answer as a single letter corresponding to the chosen solution, without any additional explanation or commentary.
"""


REPHRASE_PROMPT = """
You are an expert at analyzing and rephrasing mathematical problems. Given a code contest problem, your task is to:

1. Carefully read and understand the problem.
2. Identify the key components: given information, constraints, and objectives.
3. Rephrase the problem in your own words, using clear and concise language.
4. Break down the problem into smaller, logical steps or parts.
5. Highlight any important details, nuances, or special cases mentioned in the problem.
6. If provided, analyze any examples to gain deeper insight into the problem's requirements.
7. Identify any implicit information or assumptions that might be crucial for solving the problem.

Present your rephrased version of the problem in a structured, bullet-point format. Ensure that your rephrasing captures all essential elements of the original problem while making it easier to understand and approach.

Problem:
{problem}
"""

