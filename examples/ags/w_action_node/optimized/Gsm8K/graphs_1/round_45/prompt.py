THINK_PROMPT = """
Please reason step by step, think about what you know and what you need to solve.
"""

REPHRASE_PROMPT = """
Please rephrase the given problem in a different way, maintaining its core meaning but potentially revealing new aspects or approaches to solve it.
"""

SELF_REVIEW_PROMPT = """
Please review your solution critically. Consider the following:
1. Does it directly address the problem?
2. Are all steps logical and necessary?
3. Are there any calculation errors?
4. Can any part be simplified or clarified?

If you find any issues, please revise your solution accordingly.
"""