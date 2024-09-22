SC_ENSEMBLE_PROMPT = """
Given the question described as follows: {question}
Several solutions have been generated to address the given question. They are as follows:
{solutions}

Carefully evaluate these solutions and identify the answer that appears most frequently across them. This consistency in answers is crucial for determining the most reliable solution.

In the "thought" field, provide a detailed explanation of your thought process. In the "solution_letter" field, output only the single letter ID (A, B, C, etc.) corresponding to the most consistent solution. Do not include any additional text or explanation in the "solution_letter" field.
"""

PYTHON_CODE_VERIFIER_PROMPT = """
You are a professional Python programmer. Your task is to write code based on a given mathematical problem and output the answer.
Always provide complete, self-contained code rather than just suggestions or partial modifications. Your code should include all necessary imports and dependencies, and be ready to run without additional setup or environment configuration.
Problem description: {problem}
Other analysis:{analysis}
Your code should:
1. Implement the calculation steps described in the problem
2. Define a function named 'solve' that outputs the result of the calculation
3. Print the final result of the calculation
Please ensure your code is efficient, well-commented, and follows Python best practices.
Do not output any code blocks.
"""