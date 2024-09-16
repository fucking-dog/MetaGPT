GENERATE_PROMPT = """
Generate a comprehensive and step-by-step solution for the following mathematical problem:

{problem}

Please follow these guidelines:
1. Begin by clearly stating the given information and what needs to be found.
2. Break down the problem into smaller, manageable steps.
3. Explain each step of your reasoning process in detail.
4. Show all relevant calculations and formulas used.
5. If applicable, include diagrams or visual representations to clarify concepts.
6. Double-check your work for accuracy and consistency.
7. Provide a clear final answer, highlighting it for easy identification.
8. If there are multiple possible approaches, briefly mention alternative methods.

Your solution should be thorough, precise, and easy to follow for someone learning the concept.
"""


CONTEXTUAL_GENERATE_PROMPT = """
Analyze and solve the given mathematical problem:

Problem: {problem}

Relevant Context: {context}

Follow these steps to provide a comprehensive solution:
1. Identify and list all given information and unknowns.
2. Determine the most appropriate mathematical concepts, formulas, or theorems to apply.
3. Present a clear, step-by-step solution:
   - Write out each calculation explicitly
   - Explain the reasoning behind each step
   - Use algebraic manipulations when necessary
4. Arrive at a final answer or conclusion.
5. Verify your solution by checking units, magnitude, and reasonableness.

Ensure your response is logically structured, mathematically accurate, and easy to follow. Be concise yet thorough in your explanations.
"""


REVIEW_PROMPT = """
Analyze the given problem: {problem}

Now, evaluate this proposed solution: {solution}

Your task is to critically assess whether the solution effectively addresses the problem. Consider these key aspects:

1. Mathematical precision and correctness
2. Completeness of the solution (all parts of the problem addressed)
3. Logical structure and clear step-by-step reasoning
4. Appropriate application of relevant mathematical concepts, formulas, and techniques
5. Efficiency of the approach (if multiple valid methods exist)

Provide a boolean review result:
- True if the solution is mathematically accurate, complete, logically sound, and effectively solves the problem
- False if there are any errors, omissions, inefficiencies, or significant areas for improvement

Include concise feedback explaining your decision. If True, highlight the solution's strengths. If False, clearly identify the specific issues or areas needing improvement.
"""


REVISE_PROMPT = """
Given the mathematical problem: {problem}

And the initial solution: {solution}

Consider the following review feedback: {feedback}

Please perform the following steps:
1. Analyze the initial solution and the feedback carefully.
2. Identify any errors or areas of improvement mentioned in the feedback.
3. Revise the solution, addressing each point raised in the feedback.
4. Ensure the revised solution is mathematically correct and complete.
5. If the original solution was correct and the feedback suggests no changes, state that the original solution stands.

Provide a clear, step-by-step revised solution that addresses all aspects of the problem and incorporates the feedback.
"""


FU_ENSEMBLE_PROMPT = """
### Problem
{problem}

### Solution Candidates
<solutions>
{solutions}
</solutions>

### Task
Analyze the given problem and solution candidates to create an optimized, comprehensive solution:

1. Evaluate each solution candidate:
   - Identify strengths and weaknesses
   - Assess accuracy and completeness
   - Consider innovative approaches

2. Synthesize the best elements:
   - Combine effective strategies from different solutions
   - Address any gaps or inconsistencies
   - Ensure logical flow and coherence

3. Enhance the integrated solution:
   - Incorporate additional insights or methods if necessary
   - Optimize for efficiency and clarity
   - Ensure the solution fully addresses all aspects of the problem

4. Provide the final, optimized solution:
   - Present a clear, step-by-step approach
   - Explain key decisions or methods used
   - Verify the solution's correctness and completeness

Aim for a solution that is not only mathematically correct but also clear, efficient, and comprehensive.
"""


MD_ENSEMBLE_PROMPT = """
As an expert judge in a coding competition, your task is to evaluate multiple solutions to this problem:

{problem}

Analyze these candidate solutions:
{solutions}

Evaluate each solution based on these criteria:
1. Correctness: Does it fully solve the problem without errors?
2. Efficiency: Is it optimized for time and space complexity?
3. Readability: Is the code clear, well-structured, and easy to understand?
4. Robustness: Does it handle edge cases and potential errors effectively?
5. Scalability: Can the solution handle larger inputs or more complex scenarios?

Consider trade-offs between these criteria. A slightly less efficient but more readable and robust solution might be preferable in some cases.

After thorough analysis, select the best overall solution. Provide your decision by writing only the chosen solution letter.
"""


SC_ENSEMBLE_PROMPT = """
You are an expert mathematical problem solver tasked with selecting the most accurate solution from multiple attempts to solve this problem: {problem}

Carefully examine the following proposed solutions:

{solutions}

Your task:
1. Analyze each solution critically, considering mathematical accuracy, logical consistency, and completeness.
2. Identify the solution that appears most frequently or has the strongest consensus among the options.
3. If there's a tie, prioritize the solution with the most detailed and logically sound explanation.
4. If no clear consensus exists, select the solution that best aligns with established mathematical principles and problem-solving techniques.
5. Respond only with the letter (A, B, C, etc.) corresponding to the best solution.

Provide only the letter of the chosen solution without any additional explanation or text.
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
For the question described as {problem_description},
please extract a short and concise answer contains only one word/few words from the following solution: {solution}.

1.Format the answer as a numerical value only.
2.Do not include any units, words, or formatting.
3.Submit the pure number that represents the solution to the problem described above.
"""