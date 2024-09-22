SOLVE_PROMPT = """
Solve the given math problem step by step. Show your work clearly, including all calculations. At the end, provide the final numerical answer as a single number, prefixed with 'Final Answer: '.

For example:
Problem: If a train travels at 60 mph for 2 hours, how far does it go?
Solution:
1. Understand the given information:
   - Speed of the train = 60 mph
   - Time of travel = 2 hours

2. Use the formula: Distance = Speed × Time
   Distance = 60 mph × 2 hours
   Distance = 120 miles

Final Answer: 120

Now, solve the given problem using this format.
"""

REVIEW_PROMPT = """
Review the given solution to the math problem. Check for any errors in calculations or reasoning. If you find any mistakes, correct them and provide the revised solution. If the solution is correct, simply confirm it. Always end your response with the final numerical answer prefixed with 'Final Answer: '.

Example:
Problem: If a train travels at 60 mph for 2 hours, how far does it go?
Solution: 
1. Understand the given information:
   - Speed of the train = 60 mph
   - Time of travel = 2 hours

2. Use the formula: Distance = Speed × Time
   Distance = 60 mph × 2 hours
   Distance = 120 miles

Final Answer: 120

Review: The solution is correct. The calculation and reasoning are accurate.
Final Answer: 120

Now, review the given solution using this format.
"""