THINK_PROMPT = """
Please reason step by step, think about what you know and what you need to solve. Consider both the original problem and the rephrased version to gain a comprehensive understanding.
"""

CONTEXT_CHECK_PROMPT = """
Analyze the given problem and determine if it requires external knowledge or context beyond basic mathematical operations and common sense reasoning. Answer with 'Yes' if external context is needed, or 'No' if it can be solved with general knowledge and logic.
"""

EXTERNAL_CONTEXT = """
[Include relevant external context or knowledge base here]
"""