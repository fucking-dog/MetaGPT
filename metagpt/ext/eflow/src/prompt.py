GENERATE_PROMPT = "{problem}\nGenerate an answer to this question, without any additional test cases. "

SC_ENSEMBLE_PROMPT = """
Given the question described as follows: {question}
Several solutions have been generated to address the given question. They are as follows:
{solutions}

Carefully evaluate these solutions and identify the answer that appears most frequently across them. This consistency in answers is crucial for determining the most reliable solution.

In the "thought" field, provide a detailed explanation of your thought process. In the "solution_letter" field, output only the single letter ID (A, B, C, etc.) corresponding to the most consistent solution. Do not include any additional text or explanation in the "solution_letter" field.
"""

AGGREGATE_PROMPT = """
Given the question described as follows: {question}
Several solutions have been generated to address the given question. They are as follows:
{solutions}

You have been provided with a set of responses from various large language models to the given problem. 
Your task is to synthesize these responses into a single, high-quality response. 
It is crucial to critically evaluate the information provided in these responses, recognizing that some of it may be incorrect. 
Your response should not simply replicate the given answers but should offer a refined, accurate, and comprehensive reply to the problem.
Ensure your response's format is consistent with the given answers, and adheres to the highest standards of accuracy and reliability.

In the "thought" field, provide a detailed explanation of your thought process. 
In the "solution" field, output your refined, accurate, and comprehensive reply to the problem.
"""

REFLECTION_ON_PUBLIC_TEST_PROMPT = """
Given a code problem and a python code solution which failed to pass test or execute, you need to analyze the reason for the failure and propose a better code solution.: 
### problem
{problem}

### Code Solution
{solution}

### Execution Result
{exec_pass}

#### Failed Test Case
{test_fail}

Please provide a reflection on the failed test cases and code solution, followed by a better code solution without any additional text or test cases.
"""

VISUAL_FEEDBACK_PROMPT = """
Given a user query and an image of the current plot, please determine whether the plot has faithfully followed the user query. 
Your task is to provide instruction to make sure the plot has strictly completed the requirements of the query. 
Please output a detailed step by step instruction on how to use python code to enhance the plot.

Here is the user query: {query} 
Carefully read and analyze the user query to understand the specific requirements. 
Check if the plot aligns with the user query in terms of data selection, plot type, and any specific customization. 
Look at the provided image of the plot. Assess the plot type, the data it represents, labels, titles, colors, and any other visual elements. 
Compare these elements with the requirements specified in the user query. Note any differences between the user query requirements and the current plot. 
Based on the identified discrepancies, provide step-by-step instructions on how to modify the Python code to meet the user query requirements. 
Suggest improvements for better visualization practices, such as clarity, readability, and aesthetics, while ensuring the primary focus is on meeting the user s specified requirements.

In the thought field, provide your whole thought process. And in the feedback field, provide the textual feedback for the plot.
"""


PYTHON_VISUALIZATION_PROMPT = """
You are a professional Python programmer. Your task is to write complete, self-contained code based on a given visualization query and output the generated image path. 
The code should include all necessary imports and dependencies, and be ready to run without additional setup or environment configuration.

Here is the query and other analysis: 
Query: {query}
Other analysis: {analysis}
{feedback}

Your code should:
1. Implement the calculation steps described in the problem.
2. Define a function named `visualize` that performs the calculation and returns the result. The `visualize` function should not require any input parameters; instead, it should obtain all necessary inputs from within the function or from globally defined variables.
3. `visualize` function return the full image path.

If the query requires data manipulation from a csv file, process the data from the csv file {csv_file} and draw the plot in one piece of code. 
When you complete a plot, remember to save it to a png file. The file path should be {file_path}

Please ensure your code is efficient, well-commented, and follows Python best practices. The output should be limited to basic data types such as strings, integers, and floats. It is prohibited to transmit images or other file formats. The code output is intended for a text-based language model.

In the thought field, provide detailed thoughts on the code and the plot.
In the code field. only provide the code, without any additional text or comments.
"""

PYTHON_CODE_PROMPT = """
这里应该实现的是任何Query，而不是可视化的，可视化的一个特殊需要时需要有确定的input与output
"""