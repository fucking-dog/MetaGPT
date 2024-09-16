
GENERATE_PROMPT = """
Provide a detailed, step-by-step solution for the given math problem:

{problem}

Adhere to these guidelines:
1. Begin by clearly stating the problem's given information and the specific question to be answered.
2. Before calculations, briefly outline your solution strategy.
3. Decompose the problem into a series of logical, sequential steps.
4. For each step:
   a. Explain your reasoning concisely but thoroughly.
   b. Present all calculations using proper mathematical notation.
   c. Interpret intermediate results when applicable.
5. Ensure each step follows logically from the previous one, maintaining a clear chain of reasoning.
6. Apply relevant mathematical formulas, defining any new variables or symbols.
7. If beneficial, include simple diagrams or graphs to illustrate concepts.
8. After obtaining the final answer, verify its correctness and relevance to the original question.
9. Briefly discuss the result's practical implications or significance, if applicable.
10. Conclude with a concise summary of the key solution steps and main findings.

Remember to prioritize mathematical accuracy, logical coherence, and clear communication throughout your solution.
"""


CONTEXTUAL_GENERATE_PROMPT = """
Solve the given mathematical problem step-by-step, utilizing the provided key information:

Problem: {problem}

Key Information: {context}

Solution Guidelines:
1. Analyze the problem and key information, identifying crucial mathematical concepts and formulas.
2. Outline a clear, efficient problem-solving strategy.
3. Present a concise yet comprehensive step-by-step solution.
4. Clearly explain each step, showing all necessary calculations and intermediate results.
5. Use precise mathematical notation and terminology throughout.
6. Ensure each step logically follows from the previous one.
7. If multiple approaches exist, choose the most efficient method.
8. Verify your solution by checking if it satisfies all given conditions and constraints.
9. Summarize the key findings or results concisely.

Your solution should be mathematically rigorous, logically structured, and as concise as possible while maintaining clarity.
"""


REVIEW_PROMPT = """
Evaluate the given solution for this mathematical problem: {problem}

Assess the solution based on these criteria:
1. Mathematical Accuracy: Are all calculations and steps correct?
2. Completeness: Does it address all parts of the problem?
3. Clarity: Is the reasoning clear and logical?
4. Efficiency: Is it the most optimal method?

Analyze each criterion thoroughly. Return True only if ALL criteria are fully satisfied. Otherwise, return False.

Provide concise feedback on:
- Solution strengths
- Areas for improvement (if any)
- Enhancement suggestions (if applicable)

Focus on mathematical validity and solution quality in your evaluation.
"""


REVISE_PROMPT = """
Given the mathematical problem: {problem}

Original solution: {solution}

Review feedback: {feedback}

Please provide a revised solution by following these steps:
1. Carefully analyze the original solution and review feedback.
2. Identify key issues and areas for improvement.
3. Revise the solution, focusing on:
   - Correcting mathematical errors
   - Clarifying explanations
   - Adding missing steps or reasoning
   - Improving logical flow
   - Using precise mathematical language and notation
4. If the original solution is correct and feedback suggests no changes, validate and confirm its accuracy.
5. Ensure the revised solution is complete, accurate, and clearly presented.

Present your revised solution concisely and logically, emphasizing any significant changes or improvements. If no changes are needed, briefly explain why the original solution is correct and complete.
"""

FU_ENSEMBLE_PROMPT = """
### Given problem

{problem}

### We've got a list of solutions

<solutions>
{solutions}
</solutions>

### Instructions
Analyze the given problem and solution candidates to synthesize an improved, comprehensive solution:

1. Evaluate each solution:
   - Identify correct approaches and accurate calculations
   - Spot any errors or misconceptions
   - Assess the completeness and clarity of explanations

2. Synthesize the best elements:
   - Combine correct steps from different solutions
   - Fill gaps in reasoning or calculations
   - Ensure a logical flow from problem to solution

3. Enhance the integrated solution:
   - Provide clear, step-by-step reasoning
   - Include any necessary intermediate calculations
   - Explain key concepts or methods used
   - Address all aspects of the original problem

4. Final review:
   - Verify the accuracy of the synthesized solution
   - Ensure the solution is complete and addresses the entire problem
   - Check that the explanation is clear and easy to follow

Produce a single, cohesive solution that represents the best integration of all correct approaches while addressing any shortcomings in the individual solutions.
"""


MD_ENSEMBLE_PROMPT = """
You are given a problem:
{problem}

Here is a list of possible solutions to the problem:
{solutions}

Using the inputs above, your goal is to choose the best solution to the code contest problem.
Don't just pick the most efficient solution. The main consideration is that the solution can fully solve the problem in a correct and robust manner.
Provide your final decision by writing the chosen solution letter.
"""


SC_ENSEMBLE_PROMPT = """
I have generated the following solutions to the question: {problem}

{solutions}

Evaluate these solutions.
Select the most consistent solution based on majority consensus.
Give your answer with a single id of solution (without anything else).
"""


REPHRASE_PROMPT = """
You are given a code contest problem:

### problem
{problem}

### instrcutions
Given the problem, Your Goal is:
Reflect on the problem, and describe it in your own words, in bullet points. Pay attention to small details, nuances, notes and examples in the problem description.
"""

FORMAT_PROMPT = """
For the described problem {problem},  
please extract a concise numeric answer from the following solution {solution}, without any units, and ensure that there are no additional comments or explanations in the response.
"""