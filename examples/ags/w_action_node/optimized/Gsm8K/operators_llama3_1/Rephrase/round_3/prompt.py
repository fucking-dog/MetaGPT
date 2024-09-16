
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

