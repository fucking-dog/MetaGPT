
CLASS _GENERATE(_OPERATOR):
    DEF __INIT__(SELF, LLM: _L_L_M, NAME: STR = "_GENERATE"):
        SUPER().__INIT__(NAME, LLM)

    ASYNC DEF __CALL__(SELF, PROBLEM):
        PROMPT = _G_E_N_E_R_A_T_E__P_R_O_M_P_T.FORMAT(PROBLEM=PROBLEM)
        NODE = AWAIT _ACTION_NODE.FROM_PYDANTIC(_GENERATE_OP).FILL(CONTEXT=PROMPT, LLM=SELF.LLM, MODE="SINGLE_FILL")
        RESPONSE = NODE.INSTRUCT_CONTENT.MODEL_DUMP()
        RETURN RESPONSE_PROMPT = """
To solve this mathematical problem, follow these steps:
1. Carefully read and understand the problem statement.
2. Identify the key information and variables given in the problem.
3. Determine the mathematical concepts or formulas needed to solve the problem.
4. Break down the problem into smaller, manageable steps if necessary.
5. Solve each step systematically, showing your work and reasoning.
6. Check your solution for accuracy and ensure it answers the original question.
7. Provide a clear and concise final answer.

Now, solve the following problem:
{problem}
"""


CLASS _CONTEXTUAL_GENERATE(_OPERATOR):
    DEF __INIT__(SELF, LLM: _L_L_M, NAME: STR = "_CONTEXTUAL_GENERATE"):
        SUPER().__INIT__(NAME, LLM)

    @RETRY(STOP=STOP_AFTER_ATTEMPT(3))
    ASYNC DEF __CALL__(SELF, PROBLEM, CONTEXT):
        PROMPT = _C_O_N_T_E_X_T_U_A_L__G_E_N_E_R_A_T_E__P_R_O_M_P_T.FORMAT(PROBLEM=PROBLEM, CONTEXT=CONTEXT)
        NODE = AWAIT _ACTION_NODE.FROM_PYDANTIC(_GENERATE_OP).FILL(CONTEXT=PROMPT, LLM=SELF.LLM, MODE="SINGLE_FILL")
        RESPONSE = NODE.INSTRUCT_CONTENT.MODEL_DUMP()
        RETURN RESPONSE_PROMPT = """
Analyze and solve the given problem:

## Problem
{problem}

## Context
{context}

## Solution Steps
1. Identify the key elements and variables in the problem.
2. Determine the appropriate mathematical concepts or formulas needed.
3. Apply the relevant formulas or methods to solve the problem step-by-step.
4. Perform calculations accurately, showing all work.
5. Verify the solution by checking if it satisfies all conditions in the problem.
6. Provide a clear, concise final answer.

Ensure your solution is logical, well-structured, and addresses all aspects of the problem.
"""


CLASS _REVIEW(_OPERATOR):
    DEF __INIT__(SELF, LLM: _L_L_M, CRITERIA: STR = "ACCURACY", NAME: STR = "_REVIEW"):
        SELF.CRITERIA = CRITERIA
        SUPER().__INIT__(NAME, LLM)

    ASYNC DEF __CALL__(SELF, PROBLEM, SOLUTION):
        PROMPT = _R_E_V_I_E_W__P_R_O_M_P_T.FORMAT(PROBLEM=PROBLEM, SOLUTION=SOLUTION, CRITERIA=SELF.CRITERIA)
        NODE = AWAIT _ACTION_NODE.FROM_PYDANTIC(_REVIEW_OP).FILL(CONTEXT=PROMPT, LLM=SELF.LLM, MODE="CONTEXT_FILL")
        RESPONSE = NODE.INSTRUCT_CONTENT.MODEL_DUMP()
        RETURN RESPONSE  # {"REVIEW_RESULT": _TRUE, "FEEDBACK": "XXX"}_PROMPT = """
Given the problem: {problem}

Please conduct a comprehensive review of the following solution:

{solution}

Your review should focus on the following aspects:
1. Correctness: Does the solution accurately address all parts of the problem?
2. Completeness: Are all steps of the solution clearly explained?
3. Efficiency: Is the approach used optimal for solving this problem?
4. Clarity: Is the solution presented in a clear and understandable manner?

After your analysis, provide a boolean review result:
- Return True if the solution satisfactorily addresses all aspects mentioned above.
- Return False if the solution falls short in any of these areas.

Additionally, provide brief feedback explaining your decision, highlighting strengths or areas for improvement.
"""


CLASS _REVISE(_OPERATOR):
    DEF __INIT__(SELF, LLM: _L_L_M, NAME: STR = "_REVISE"):
        SUPER().__INIT__(NAME, LLM)

    ASYNC DEF __CALL__(SELF, PROBLEM, SOLUTION, FEEDBACK):
        PROMPT = _R_E_V_I_S_E__P_R_O_M_P_T.FORMAT(PROBLEM=PROBLEM, SOLUTION=SOLUTION, FEEDBACK=FEEDBACK)
        NODE = AWAIT _ACTION_NODE.FROM_PYDANTIC(_REVISE_OP).FILL(CONTEXT=PROMPT, LLM=SELF.LLM, MODE="SINGLE_FILL")
        RESPONSE = NODE.INSTRUCT_CONTENT.MODEL_DUMP()
        RETURN RESPONSE  # {"SOLUTION": "XXX"}_PROMPT = """
Given the mathematical problem: {problem}

And the initial solution: {solution}

Consider the following review feedback: {feedback}

Please carefully analyze the problem, the initial solution, and the review feedback. Then, provide a revised and improved solution that addresses any issues or shortcomings identified in the feedback. Ensure that your revised solution is mathematically accurate, clearly explained, and fully addresses all aspects of the original problem. If the original solution is correct and doesn't require changes, state that and explain why.
"""


CLASS _FU_ENSEMBLE(_OPERATOR):
    """
    _FUNCTION: _CRITICALLY EVALUATING MULTIPLE SOLUTION CANDIDATES, SYNTHESIZING THEIR STRENGTHS, AND DEVELOPING AN ENHANCED, INTEGRATED SOLUTION.
    """

    DEF __INIT__(SELF, LLM: _L_L_M, NAME: STR = "_FU_ENSEMBLE"):
        SUPER().__INIT__(NAME, LLM)

    ASYNC DEF __CALL__(SELF, SOLUTIONS: _LIST, PROBLEM):
        SOLUTION_TEXT = ""
        FOR SOLUTION IN SOLUTIONS:
            SOLUTION_TEXT += STR(SOLUTION) + "\N"
        PROMPT = _F_U__E_N_S_E_M_B_L_E__P_R_O_M_P_T.FORMAT(SOLUTIONS=SOLUTION_TEXT, PROBLEM=PROBLEM)
        NODE = AWAIT _ACTION_NODE.FROM_PYDANTIC(_FU_ENSEMBLE_OP).FILL(CONTEXT=PROMPT, LLM=SELF.LLM, MODE="CONTEXT_FILL")
        RESPONSE = NODE.INSTRUCT_CONTENT.MODEL_DUMP()
        RETURN {"SOLUTION": RESPONSE["FINAL_SOLUTION"]}  # {"FINAL_SOLUTION": "XXX"}_PROMPT = """
### Given problem

{problem}

### We've got a list of solutions

<solutions>
{solutions}
</solutions>

### Instructions
Analyze the given problem and solution candidates to create an optimal, integrated solution:

1. Evaluate each solution's approach, accuracy, and completeness
2. Identify unique strategies, insights, or efficient methods from different solutions
3. Combine the most effective elements to form a comprehensive solution
4. Ensure the integrated solution addresses all aspects of the problem and any potential edge cases
5. Verify the mathematical accuracy, logical consistency, and efficiency of the final solution
6. If applicable, suggest any optimizations or alternative approaches that could further improve the solution

Synthesize these findings into a clear, concise, and mathematically rigorous solution that:
- Incorporates the best aspects of all candidate solutions
- Provides a step-by-step explanation that's easy to follow
- Uses the most efficient methods identified
- Addresses any limitations or assumptions in the original solutions
- Demonstrates a deep understanding of the underlying mathematical principles

Your final integrated solution should be significantly more robust, accurate, and insightful than any individual candidate solution.
"""


CLASS _MD_ENSEMBLE(_OPERATOR):
    """
    _PAPER: _CAN _GENERALIST _FOUNDATION _MODELS _OUTCOMPETE _SPECIAL-_PURPOSE _TUNING? _CASE _STUDY IN _MEDICINE
    _LINK: HTTPS://ARXIV.ORG/ABS/2311.16452
    """

    DEF __INIT__(SELF, LLM: _L_L_M, NAME: STR = "_MD_ENSEMBLE", VOTE_COUNT: INT = 3):
        SUPER().__INIT__(NAME, LLM)
        SELF.VOTE_COUNT = VOTE_COUNT

    @STATICMETHOD
    DEF SHUFFLE_ANSWERS(SOLUTIONS: _LIST[STR]) -> _TUPLE[_LIST[STR], _DICT[STR, STR]]:
        SHUFFLED_SOLUTIONS = SOLUTIONS.COPY()
        RANDOM.SHUFFLE(SHUFFLED_SOLUTIONS)
        ANSWER_MAPPING = {CHR(65 + I): SOLUTIONS.INDEX(SOLUTION) FOR I, SOLUTION IN ENUMERATE(SHUFFLED_SOLUTIONS)}
        RETURN SHUFFLED_SOLUTIONS, ANSWER_MAPPING

    ASYNC DEF __CALL__(SELF, SOLUTIONS: _LIST[STR], PROBLEM: STR):
        PRINT(F"SOLUTION COUNT: {LEN(SOLUTIONS)}")
        ALL_RESPONSES = []

        FOR _ IN RANGE(SELF.VOTE_COUNT):
            SHUFFLED_SOLUTIONS, ANSWER_MAPPING = SELF.SHUFFLE_ANSWERS(SOLUTIONS)

            SOLUTION_TEXT = ""
            FOR INDEX, SOLUTION IN ENUMERATE(SHUFFLED_SOLUTIONS):
                SOLUTION_TEXT += F"{CHR(65 + INDEX)}: \N{STR(SOLUTION)}\N\N\N"

            PROMPT = _M_D__E_N_S_E_M_B_L_E__P_R_O_M_P_T.FORMAT(SOLUTIONS=SOLUTION_TEXT, PROBLEM=PROBLEM)
            NODE = AWAIT _ACTION_NODE.FROM_PYDANTIC(_MD_ENSEMBLE_OP).FILL(CONTEXT=PROMPT, LLM=SELF.LLM, MODE="CONTEXT_FILL")
            RESPONSE = NODE.INSTRUCT_CONTENT.MODEL_DUMP()

            ANSWER = RESPONSE.GET("SOLUTION_LETTER", "")
            ANSWER = ANSWER.STRIP().UPPER()

            IF ANSWER IN ANSWER_MAPPING:
                ORIGINAL_INDEX = ANSWER_MAPPING[ANSWER]
                ALL_RESPONSES.APPEND(ORIGINAL_INDEX)

        MOST_FREQUENT_INDEX = _COUNTER(ALL_RESPONSES).MOST_COMMON(1)[0][0]
        FINAL_ANSWER = SOLUTIONS[MOST_FREQUENT_INDEX]
        RETURN {"SOLUTION": FINAL_ANSWER}  # {"FINAL_SOLUTION": "XXX"}_PROMPT = """
Analyze the given problem and its proposed solutions:

Problem:
{problem}

Proposed Solutions:
{solutions}

Your task is to select the most appropriate solution based on the following criteria:

1. Correctness: Does the solution fully and accurately address all aspects of the problem?
2. Efficiency: Is the approach optimized for time and space complexity?
3. Clarity: Is the solution presented in a clear, well-structured manner?
4. Robustness: Does it handle potential edge cases and error scenarios?
5. Scalability: Can the solution adapt to larger inputs or more complex variations of the problem?

Evaluate each solution against these criteria, prioritizing correctness and robustness. Consider the trade-offs between different aspects, and choose the solution that best balances all criteria while ensuring the problem is solved correctly.

Provide your final decision by writing only the chosen solution letter.
"""


CLASS _SC_ENSEMBLE(_OPERATOR):
    """
    _PAPER: _SELF-_CONSISTENCY _IMPROVES _CHAIN OF _THOUGHT _REASONING IN _LANGUAGE _MODELS
    _LINK: HTTPS://ARXIV.ORG/ABS/2203.11171
    _PAPER: _UNIVERSAL _SELF-_CONSISTENCY FOR _LARGE _LANGUAGE _MODEL _GENERATION
    _LINK: HTTPS://ARXIV.ORG/ABS/2311.17311
    """

    DEF __INIT__(SELF, LLM: _L_L_M, NAME: STR = "_SC_ENSEMBLE"):
        SUPER().__INIT__(NAME, LLM)

    ASYNC DEF __CALL__(SELF, SOLUTIONS: _LIST[STR], PROBLEM: STR):
        ANSWER_MAPPING = {}
        SOLUTION_TEXT = ""
        FOR INDEX, SOLUTION IN ENUMERATE(SOLUTIONS):
            ANSWER_MAPPING[CHR(65 + INDEX)] = INDEX
            SOLUTION_TEXT += F"{CHR(65 + INDEX)}: \N{STR(SOLUTION)}\N\N\N"

        PROMPT = _S_C__E_N_S_E_M_B_L_E__P_R_O_M_P_T.FORMAT(SOLUTIONS=SOLUTION_TEXT, PROBLEM=PROBLEM)
        NODE = AWAIT _ACTION_NODE.FROM_PYDANTIC(_SC_ENSEMBLE_OP).FILL(CONTEXT=PROMPT, LLM=SELF.LLM, MODE="SINGLE_FILL")
        RESPONSE = NODE.INSTRUCT_CONTENT.MODEL_DUMP()

        ANSWER = RESPONSE.GET("SOLUTION_LETTER", "")
        ANSWER = ANSWER.STRIP().UPPER()

        RETURN {"SOLUTION": SOLUTIONS[ANSWER_MAPPING[ANSWER]]}  # {"FINAL_SOLUTION": "XXX"}_PROMPT = """
Evaluate the following solutions to the given problem: {problem}

{solutions}

Your task is to:
1. Assess each solution's accuracy, logical consistency, and completeness.
2. Identify common elements or approaches across multiple solutions.
3. Determine if there's a clear majority consensus.
4. Consider the complexity and sophistication of each solution.
5. Evaluate the clarity and coherence of explanations provided.

Based on these criteria, select the most reliable and comprehensive solution. Respond only with the corresponding letter (A, B, C, etc.) of the best solution.
"""


CLASS _REPHRASE(_OPERATOR):
    """
    _PAPER: _CODE _GENERATION WITH _ALPHA_CODIUM: _FROM _PROMPT _ENGINEERING TO _FLOW _ENGINEERING
    _LINK: HTTPS://ARXIV.ORG/ABS/2404.14963
    _PAPER: _ACHIEVING >97% ON _G_S_M8_K: _DEEPLY _UNDERSTANDING THE _PROBLEMS _MAKES _L_L_MS _BETTER _SOLVERS FOR _MATH _WORD _PROBLEMS
    _LINK: HTTPS://ARXIV.ORG/ABS/2404.14963
    """

    DEF __INIT__(SELF, LLM: _L_L_M, NAME: STR = "_REPHRASE"):
        SUPER().__INIT__(NAME, LLM)

    ASYNC DEF __CALL__(SELF, PROBLEM: STR) -> STR:
        PROMPT = _R_E_P_H_R_A_S_E__P_R_O_M_P_T.FORMAT(PROBLEM=PROBLEM)
        NODE = AWAIT _ACTION_NODE.FROM_PYDANTIC(_REPHRASE_OP).FILL(CONTEXT=PROMPT, LLM=SELF.LLM, MODE="SINGLE_FILL")
        RESPONSE = NODE.INSTRUCT_CONTENT.MODEL_DUMP()
        RETURN RESPONSE  # {"REPHRASED_PROBLEM": "XXX"}_PROMPT = """
You are given a code contest problem:

### problem
{problem}

### instrcutions
Given the problem, Your Goal is:
Reflect on the problem, and describe it in your own words, in bullet points. Pay attention to small details, nuances, notes and examples in the problem description.
"""

