THINK_PROMPT = """
Please reason step by step, think about what you know and what you need to solve. Consider both the original problem and the rephrased version to gain a comprehensive understanding.
"""

SELF_ASK_PROMPT = """
Based on your initial thoughts, ask yourself the following questions:
1. Are there any assumptions I've made that I should question?
2. Is there a different approach or perspective I haven't considered?
3. Are there any potential edge cases or special conditions I should account for?
4. Is there any additional information or context that would be helpful in solving this problem?

Provide brief answers to these questions, focusing on aspects that weren't fully addressed in your initial thinking."""