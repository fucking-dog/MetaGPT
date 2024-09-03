THINK_PROMPT = """
Please reason step by step, think about what you know and what you need to solve. After your initial thoughts, ask yourself two critical questions about the problem that could lead to a deeper understanding or reveal potential solution approaches. Then, answer these questions to the best of your ability.
"""

REPHRASE_PROMPT = """
Please rephrase the given problem in a different way, maintaining its core meaning but potentially revealing new aspects or approaches to solve it.
"""

REFLECT_PROMPT = """
Reflect on the solution you've just generated. Consider the following:
1. Does this solution fully address all aspects of the problem?
2. Are there any potential weaknesses or edge cases in this solution?
3. Can you think of any alternative approaches that might be more efficient or effective?
Provide a brief reflection on these points.
"""