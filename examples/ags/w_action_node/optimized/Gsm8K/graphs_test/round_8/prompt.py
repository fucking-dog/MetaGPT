SOLVE_PROMPT_1 = """
Solve the given math problem step by step using the specified approach. Show your work and explain each step clearly.
Approach: {approach}
Problem: {problem}
Provide a detailed solution using the given approach.
"""

SOLVE_PROMPT_2 = """
Tackle the following mathematical problem using the indicated approach. Break down your solution into clear, logical steps, ensuring each part of your reasoning is thoroughly explained.
Approach: {approach}
Problem: {problem}
Present a comprehensive solution that demonstrates your problem-solving process.
"""

REVIEW_PROMPT = """
Review the initial solution to the math problem. Check for any errors or areas that need improvement. If you find any issues, provide a corrected and improved solution. If the initial solution is correct, confirm its accuracy and completeness.
"""

SELECT_BEST_PROMPT = """
Given the following problem and multiple solutions, analyze each solution and select the best one. Consider factors such as correctness, clarity of explanation, and efficiency of the approach. Provide the selected best solution along with a brief explanation of why it was chosen.
"""

REFINE_PROMPT = """
Given the reviewed solution, refine and improve it further. Focus on enhancing clarity, conciseness, and mathematical rigor. Ensure all steps are logically connected and well-explained. If possible, provide alternative methods or insights that could deepen understanding of the problem.
"""