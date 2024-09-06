THINK_PROMPT = """
Please reason step by step, think about what you know and what you need to solve.
"""

REPHRASE_PROMPT = """
Please rephrase the given problem in a different way, maintaining its core meaning but using alternative wording or structure. This rephrasing should provide a fresh perspective on the problem.
"""

SELF_ASK_PROMPT = """
Based on your initial thoughts, what additional questions should you ask yourself to gain a deeper understanding of the problem? List these questions and provide brief answers to each.
"""

SELF_REFLECT_PROMPT = """
Carefully examine the solution and the review feedback. Identify any weaknesses or areas for improvement in the solution. Then, suggest specific modifications or enhancements to address these issues and strengthen the overall solution.
"""

REVISE_PROMPT = """
Based on the review feedback and self-reflection, please revise the solution to address the identified issues and improve its overall quality. Ensure that your revised solution is comprehensive and addresses all aspects of the problem.
"""

VERIFY_PROMPT = """
Please verify the mathematical correctness of the given solution. Check for any calculation errors, logical inconsistencies, or violations of mathematical principles. If you find any issues, briefly describe them.
"""