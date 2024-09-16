
CONTEXTUAL_GENERATE_PROMPT = """
Solve the given mathematical problem using the provided context:

## Problem
{problem}

## Context
{context}

## Solution Approach
1. Analyze the problem and context to identify crucial information and variables.
2. Select the appropriate mathematical concepts, formulas, or methods required for solving.
3. Develop a step-by-step solution, clearly explaining each stage of the process.
4. Execute calculations with precision, showing all necessary work.
5. Validate your solution by ensuring it meets all problem conditions and constraints.
6. Summarize the final answer concisely and accurately.

Remember to:
- Use logical reasoning and mathematical principles throughout your solution.
- Explain your thought process and justify any assumptions made.
- Consider alternative approaches if applicable.
- Highlight any key insights or patterns discovered during problem-solving.

Provide a comprehensive, well-structured solution that addresses all aspects of the problem.
"""

