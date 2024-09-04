Generate_PROMPT = """
Generate Solution for the following problem: {problem}
"""

FORMAT_PROMPT = """
For the question described as {problem},
please extract a short and concise answer contains only one word/few words from the following solution: {solution}.
Make sure there are no additional comments or explanations in your response.
"""


ContextualGenerate_PROMPT = """
Generate Solution for the following problem: 

## Problem Description
{problem}

## Thought
{context}
"""

REVIEW_PROMPT = """
For the question described as {problem},
please review the following solution: {solution}, and provide a review result in boolean format.
```
You will be reviewing the problem-solving process of another AI assistant that has answered a mathematical question. Your task is to evaluate the solution and provide a detailed review for refinement. Follow these steps:
<step1>
Carefully read through the original question and entire solution, paying close attention to the relevant concepts, thinking process, calculations, and final result. Assess whether the solution is clear, logical, and well-organized. Write your initial review in <initialReview> tags.
</step1>
<step2>
Evaluate the reasoning and logic behind the solution. Ensure that the thinking process is clear, coherent, and mathematically sound. If you find any areas that need clarification or improvement, provide your suggestions inside <reasoningFeedback> tags.
</step2>
<step3>
Re-do the calculations presented in the <calculation> section **carefully and step-by-step** to verify the accuracy. Break down the calculations into the simplest possible steps and check each step for errors. You must not be careless and treat every part with rigor. Don't neglect checking any calculation part of the solution process. If you find any mistakes, note them down inside <calculationErrors> tags.
</step3>
<step4>
Provide an overall assessment of the solution's thoroughness, accuracy, and clarity inside <overallAssessment> tags. Highlight the strengths and weaknesses of the solution and offer suggestions for improvement, if any.
</step4>
use XML tags to present your complete evaluation, including initial review, calculation errors, reasoning feedback, and overall assessment, in a well-organized and easy-to-follow format.
Remember to be thorough, constructive, and professional in your review. Your goal is to help improve the quality and accuracy of the mathematical problem-solving process.
```
If you believe the solution is capable of resolving the issue, return True; otherwise, return False, and include your comments
"""

REVISE_PROMPT = """
For the question described as {problem},
please evaluate and revise the solution provided: {solution}, taking into account the review feedbacks: {feedback}."
Then output the revised solution.
"""

FU_ENSEMBLE_PROMPT = """
### Given problem

{problem}

### We've got a list of solutions

<solutions>
{solutions}
</solutions>

### Instructions
Based on the given problem and solution candidates:

1. Analyze the pros and cons of each candidate solution
2. Consider how to integrate reasonable parts from different solutions
3. Formulate a more comprehensive and effective solution
"""

MD_ENSEMBLE_PROMPT = """
You are given a coding problem:
{problem}

Here is a list of possible solutions to the problem:
{solutions}

Using the inputs above, your goal is to choose the best solution to the code contest problem.
Don't just pick the most efficient solution. The main consideration is that the solution can fully solve the problem in a correct and robust manner.
Provide your final decision by writing the chosen solution letter.

Please maintain the JSON format in your response.
"""

SC_ENSEMBLE_PROMPT = """
I have generated the following solutions to the question: {problem}

{solutions}

Evaluate these solutions.
Select the most consistent solution based on majority consensus.
Give your answer with a single id of solution (without anything else).
"""

REPHRASE_ON_PROBLEM_PROMPT = """
You are given a code contest problem:

### problem
{problem}

### instrcutions
Given the problem, Your Goal is:
Reflect on the problem, and describe it in your own words, in bullet points. Pay attention to small details, nuances, notes and examples in the problem description.
"""


CRITICAL_MATH_SOLVE_PROMPT = """You are a critical thinking math expert. Your task is to solve the following mathematical problem using critical thinking principles. Follow these steps:

1. Question the problem: Identify key information and any assumptions.
2. Break down the problem into smaller parts.
3. For each part:
   a. Propose a solution approach.
   b. Validate the approach by considering potential issues or edge cases.
   c. Apply self-inquiry by asking "Why am I using this method?" and "Is there a more efficient way?"
4. Solve each part, showing all work and explaining each step.
5. Combine the parts to form a complete solution.
6. Review the entire solution, questioning its validity and considering alternative approaches.
7. Provide a final answer.

Problem: {problem}

Present your solution in a clear, step-by-step format, including all calculations and reasoning. End with a concise final answer."""



STEP_BY_STEP_BREAKDOWN_PROMPT = """You are a math tutor tasked with breaking down complex math problems into simpler steps. Given the following math problem, please provide a step-by-step breakdown of how to approach and solve it. Each step should be clear, concise, and build upon the previous ones.

Math Problem: {problem}

Please provide your step-by-step breakdown, with each step on a new line, prefixed by "Step X:", where X is the step number."""



STEP_BY_STEP_BREAKDOWN_PROMPT = """Given the following math problem:

{problem}

Please break down this problem into a series of simpler steps. Each step should be a clear, concise instruction or sub-problem that contributes to solving the overall problem. Ensure that:

1. The steps are in a logical order.
2. Each step is simple enough to be easily understood and solved.
3. The combination of all steps leads to the solution of the original problem.
4. You include any necessary intermediate calculations or transformations.

Provide your breakdown as a numbered list of steps."""



MATH_STEP_BREAKDOWN_PROMPT = """You are a math tutor tasked with breaking down complex math problems into simpler steps. Given the following math problem, please provide a step-by-step breakdown of how to approach and solve it. Each step should be clear, concise, and logically connected to the next.

Math Problem: {problem}

Please provide your step-by-step breakdown, with each step on a new line, prefixed by "Step X:" where X is the step number."""



MATH_ANALYZE_PROMPT = """Given the following math problem:

{problem}

Please analyze the problem and provide the following:

1. Key components: List the main mathematical elements or concepts involved in the problem.
2. Solution strategies: Suggest potential approaches or methods to solve this problem.
3. Difficulty level: Assess the problem's difficulty as 'Easy', 'Medium', or 'Hard'.

Provide your analysis in a structured format."""



MATH_STEP_BREAKDOWN_PROMPT = """Given the following math problem:

{problem}

Please break down this problem into a series of simpler steps. Each step should be a clear, concise instruction that moves towards solving the problem. Include any necessary intermediate calculations or conceptual explanations. Format your response as a numbered list of steps.

Example format:
1. [First step]
2. [Second step]
3. [Third step]
...

Ensure that following these steps in order would lead to a complete solution of the problem."""



ANALYZE_PROMPT = """You are a math expert tasked with analyzing complex math problems. Your job is to break down the given problem into smaller, more manageable steps and identify key components that will help in solving it.

Given the following math problem:

{problem}

Please provide a detailed analysis that includes:
1. The main objective of the problem
2. Key information or given data
3. Relevant formulas or mathematical concepts needed
4. A step-by-step breakdown of how to approach the problem
5. Any potential challenges or areas that require special attention

Your analysis should be clear, concise, and helpful for someone trying to solve this problem."""



BREAK_DOWN_PROMPT = """You are a math expert tasked with breaking down complex problems into simpler steps. Given the following math problem, please break it down into a series of smaller, more manageable steps. Each step should be clear and concise, guiding the solver through the problem-solving process.

Math problem: {problem}

Provide your breakdown in the following format:
Step 1: [Description of first step]
Step 2: [Description of second step]
...and so on.

Ensure that your steps are logically ordered and cover all necessary parts of the problem."""



DECOMPOSE_PROMPT = """You are a mathematical problem-solving assistant. Your task is to decompose the given complex math problem into smaller, more manageable sub-problems. Each sub-problem should be a distinct step that contributes to solving the overall problem.

Problem: {problem}

Please provide a list of sub-problems, each representing a step towards solving the main problem. Ensure that:
1. Each sub-problem is clearly stated and self-contained.
2. The sub-problems are in a logical order that leads to the solution of the main problem.
3. Each sub-problem is simpler than the original problem.
4. The set of sub-problems, when solved in order, will lead to the solution of the main problem.

Format your response as a numbered list of sub-problems."""



STEP_BY_STEP_PROMPT = """You are a math tutor tasked with breaking down complex math problems into simpler steps. Given the following math problem, please provide a step-by-step breakdown of how to solve it. Each step should be clear, concise, and easy to understand. Do not solve the problem completely, but rather provide a roadmap for solving it.

Math Problem: {problem}

Please provide the steps to solve this problem in the following format:
1. [First step]
2. [Second step]
3. [Third step]
...and so on.

Ensure that each step is a logical progression towards the solution and that no step is too complex. If a step involves a calculation, describe the calculation without performing it."""



DECOMPOSE_PROMPT = """You are a mathematical problem-solving assistant. Your task is to break down the following complex math problem into smaller, more manageable steps. Each step should be clear, concise, and logically connected to the next. Please provide a list of steps that, when followed in order, will lead to the solution of the problem.

Problem: {problem}

Please provide your step-by-step breakdown in the following format:
1. [First step]
2. [Second step]
3. [Third step]
...and so on.

Ensure that your steps are detailed enough for someone to follow along and solve the problem independently."""



MATH_STEP_BREAKDOWN_PROMPT = """You are a math tutor tasked with breaking down complex math problems into simpler, more manageable steps. Given the following math problem, please provide a step-by-step breakdown of how to approach and solve it. Each step should be clear, concise, and build upon the previous ones.

Math Problem: {problem}

Please provide your step-by-step breakdown below:

Step 1:
Step 2:
Step 3:
...

Continue until you've fully broken down the problem into solvable steps."""



DECOMPOSE_PROMPT = """Given the following math problem:

{problem}

Please break down this problem into smaller, more manageable sub-problems. Each sub-problem should be a step towards solving the overall problem. Present your answer as a numbered list of sub-problems.

For example:
1. Calculate X
2. Determine Y
3. Apply formula Z
4. Combine results

Ensure that solving all sub-problems in order will lead to the solution of the main problem."""



DECOMPOSE_PROMPT = """Given the following math problem:

{problem}

Please decompose this problem into simpler sub-problems that can be solved step-by-step. Provide a list of sub-problems and a brief explanation of how solving these sub-problems will lead to the solution of the original problem.

Your response should include:
1. A list of sub-problems, each clearly stated and numbered.
2. A brief explanation of how these sub-problems relate to solving the original problem.

Ensure that your decomposition is logical, comprehensive, and covers all aspects of the original problem."""



MATH_SOLVER_PROMPT = """You are a mathematical problem-solving assistant. Your task is to solve the given math problem step by step. Please follow these instructions:

1. Read and understand the problem carefully.
2. Break down the solution into clear, logical steps.
3. For each step, provide a brief explanation of what you're doing and why.
4. Show all relevant calculations.
5. Double-check your work for accuracy.
6. Provide a final answer clearly stated at the end.

Here's the math problem to solve:

{problem}

Please provide your step-by-step solution with explanations."""



DECOMPOSE_PROMPT = """You are a math problem decomposition expert. Your task is to break down the given complex math problem into smaller, more manageable sub-problems. Each sub-problem should be a distinct step that contributes to solving the overall problem.

Problem description:
{problem}

Please provide a list of sub-problems, each on a new line. Ensure that solving all sub-problems in order will lead to the solution of the main problem. Be specific and clear in your decomposition.

Sub-problems:"""



DECOMPOSEMATH_PROMPT = """You are a skilled mathematics tutor. Your task is to break down the following complex math problem into simpler, sequential steps that can be solved individually. Each step should be clear, concise, and lead logically to the next. Please provide your response as a numbered list of steps.

Problem: {problem_description}

Steps to solve the problem:
1.
2.
3.
...

Remember to include all necessary intermediate steps and calculations. Your goal is to make the problem-solving process as clear and approachable as possible for a student who might be struggling with the concept."""



MATH_STEP_DECOMPOSE_PROMPT = """You are a mathematical problem-solving assistant. Your task is to break down the given complex math problem into a series of simpler, step-by-step operations. This will help in solving the problem more easily.

Given problem: {problem_description}

Please provide a list of steps to solve this problem. Each step should be a single, clear operation that moves towards the solution. Be as detailed and specific as possible.

For example, if the problem is "Solve the equation 2x + 5 = 13", your steps might be:
1. Subtract 5 from both sides of the equation
2. Simplify the equation
3. Divide both sides by 2
4. Simplify to get the final answer

Now, please decompose the given problem into a similar list of steps."""



MATH_STEP_SOLVER_PROMPT = """You are a skilled math tutor tasked with solving mathematical problems step-by-step. Your goal is to provide a clear and detailed explanation of the solution process.

Given problem: {problem}

Please solve the problem by following these instructions:
1. Break down the problem into logical steps.
2. For each step:
   - Explain the mathematical concept or operation being applied.
   - Show the calculation or transformation being performed.
   - Provide a brief explanation of why this step is necessary.
3. After completing all steps, state the final answer clearly.

Format your response as follows:
Steps:
1. [Step 1 explanation]
2. [Step 2 explanation]
...
n. [Final step explanation]

Final Answer: [State the final answer here]

Remember to be thorough in your explanations, making sure each step is clear and understandable to someone learning the concept."""



MATH_STEP_BREAKDOWN_PROMPT = """You are a math expert tasked with breaking down complex math problems into simpler, step-by-step instructions. Your goal is to make the problem-solving process more manageable and easier to understand.

Given the following math problem:

{problem}

Please break down the problem-solving process into a series of clear, concise steps. Then, provide a brief explanation of your overall approach.

Your response should be in the following format:

Steps:
1. [First step]
2. [Second step]
3. [Third step]
...

Explanation: [Brief explanation of the overall approach]

Ensure that your steps are logical, sequential, and easy to follow. Your explanation should provide insight into your problem-solving strategy."""



MATH_STEP_BREAKDOWN_PROMPT = """You are a math expert tasked with breaking down complex math problems into step-by-step solutions. Your goal is to provide a clear, detailed breakdown of the problem-solving process.

Given the following math problem:

{problem}

Please break down the solution into individual steps and provide a detailed explanation for each step. Your response should be in the following format:

Steps:
1. [First step of the solution]
2. [Second step of the solution]
3. [Third step of the solution]
...

Explanations:
1. [Detailed explanation for the first step]
2. [Detailed explanation for the second step]
3. [Detailed explanation for the third step]
...

Ensure that your steps and explanations are clear, concise, and easy to understand. Use mathematical notation where appropriate, but also provide written explanations to clarify each step of the process."""



MATH_STEP_BY_STEP_PROMPT = """You are a math tutor tasked with breaking down complex math problems into clear, step-by-step solutions. Your goal is to make the problem-solving process as understandable as possible.

Given the following math problem:

{problem}

Please provide a detailed step-by-step solution. For each step:
1. Clearly state the action being taken.
2. Show the mathematical operation or transformation.
3. Explain the reasoning behind the step.

After providing all the steps, give the final answer.

Format your response as follows:
Steps:
1. [Step 1 description and explanation]
2. [Step 2 description and explanation]
...
n. [Final step description and explanation]

Final Answer: [Provide the final answer here]

Brief Explanation: [Provide a concise summary of the solution process]"""

