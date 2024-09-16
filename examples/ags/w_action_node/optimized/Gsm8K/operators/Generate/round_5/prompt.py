
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

