REVISION_CONTEXT = """
Given the problem and the original solution, provide additional context or insights that might be helpful for revising the solution. Consider:
1. Any important mathematical concepts or formulas that might have been overlooked.
2. Potential alternative approaches to solving the problem.
3. Common pitfalls or mistakes related to this type of problem.
4. Any relevant real-world applications or examples that could enhance understanding.

Provide this context in a concise, clear manner to assist in improving the solution.
"""

ALTERNATIVE_APPROACH = """
Given the mathematical problem and its visual representation, suggest an alternative approach to solving it. This approach should be different from the most obvious or standard method. Consider:
1. Using a different mathematical technique or concept.
2. Approaching the problem from a unique angle or perspective.
3. Applying a less common but potentially more efficient method.
4. Utilizing the provided visual representation to gain new insights.

Provide a brief description of this alternative approach, focusing on its key steps or principles.
"""

VISUAL_REPRESENTATION = """
Given the mathematical problem, create a concise textual description of a visual representation or diagram that could help in understanding and solving the problem. Consider:
1. Key elements of the problem that can be visualized.
2. Relationships between different components of the problem.
3. Any geometric shapes, graphs, or charts that might be relevant.
4. How the visual representation could highlight important aspects of the problem.

Provide a clear and detailed description of the visual representation, focusing on how it relates to the problem and could aid in finding a solution.
"""

APPROACH_ANALYSIS = """
Given the mathematical problem and a list of alternative approaches, perform a comparative analysis of these approaches. Consider the following criteria:
1. Efficiency: How quickly and with how few steps can the approach solve the problem?
2. Accuracy: How likely is the approach to lead to a correct solution?
3. Applicability: How well does the approach fit the specific problem at hand?
4. Originality: Does the approach offer a unique or innovative perspective?
5. Potential for insights: Could the approach lead to deeper understanding or generalizable methods?

Based on this analysis, identify the most promising approaches (at least two) that are likely to yield the best solutions. Provide a brief explanation for your choices.
"""