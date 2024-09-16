FORMAT_PROMPT = """
For the question described as {problem},
please extract a short and concise answer contains only one number from the following solution: {solution}.

1.Format the answer as a numerical value only.
2.Do not include any units, words, or formatting.
3.Submit the pure number that represents the solution to the problem described above."""