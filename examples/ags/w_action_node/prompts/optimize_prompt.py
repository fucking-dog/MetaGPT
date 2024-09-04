OPERATOR_EXTEND_PROMPT = """
You are tasked with developing an additional operator and the corresponding prompts to collaboratively solve {type} problems.

While we typically address these issues using the provided list of operators, I'd like you to apply critical thinking principles (questioning, validating, and self-inquiry) to generate more operators capable of solving this problem.

Please present your newly created operator description, prompt, and its associated code within XML tags in your response. These will be utilized as new operator for problem-solving. Ensure that the operator is comprehensive and accurate to avoid potential runtime errors.
Keep the prompt variable name consistent with the operator's name, and append _PROMPT to it.
"""

OPERATOR_EXTEND_INPUT_PROMPT = """
Below is a list of operators and two examples of operator's code:
<sample>
    <operators>{operators}</operators>
    <code_examples>{code}</code_examples>
</sample>
"""

OPERATOR_SELECT_PROMPT = """
You are tasked with selecting {count} operators from the list of candidate operators to address {type} problems.

You will see a list of Fixed Operators that provide guidelines for your selection:

1. The selected operators should complement the Fixed Operators.
2. The selected operators should be able to collaborate with other operators within a graph represented by code.
3. The selected operators should be the most effective in solving {type} problems.

Please provide the names of the operators you have selected in the format of List in python within XML tags in your response. These operators will be used to solve the problem. Ensure that the selected operator names match those in the candidate list.
"""

OPERATOR_SELECT_INPUT_PROMPT = """
Below is the list of Fixed Operators and the list of candidate operators awaiting selection:
<sample>
    <fixed_operators>{fixed_operators}</fixed_operators>
    <candidate_operators>{candidate_operators}</candidate_operators>
</sample>
"""
# class GenerateOp(BaseModel):
#     # The Op restricts the keys of the output dictionary, which should be consistent with the Prompt you provide.
#     solution: str = Field(default="", description="Your solution for this problem")
#
# class Generate(Operator):
#     def __init__(self, llm: LLM, name: str = "Generate"):
#         super().__init__(name, llm)
#
#     async def __call__(self, problem):
#         prompt = GENERATE_PROMPT.format(problem_description=problem)
#         node = await ActionNode.from_pydantic(GenerateOp).fill(context=prompt, llm=self.llm)
#         response = node.instruct_content.model_dump()
#         return response


OPERATOR_CODE_EXAMPLES = """
class ScEnsembleOp(BaseModel):
    # The Op restricts the keys of the output dictionary, which should be consistent with the Prompt you provide.
    solution_letter: str = Field(default="", description="The letter of most consistent solution.")


class ScEnsemble(Operator):

    def __init__(self, llm: LLM, name: str = "ScEnsemble"):
        super().__init__(name, llm)

    async def __call__(self, solutions: List[str], problem: str):
        answer_mapping = {}
        solution_text = ""
        for index, solution in enumerate(solutions):
            answer_mapping[chr(65 + index)] = index
            solution_text += f"{chr(65 + index)}: \n{str(solution)}\n\n\n"

        prompt = SC_ENSEMBLE_PROMPT.format(solutions=solution_text, problem=problem)
        node = await ActionNode.from_pydantic(ScEnsembleOp).fill(context=prompt, llm=self.llm, mode="single_fill")
        response = node.instruct_content.model_dump()

        answer = response.get("solution_letter", "")
        answer = answer.strip().upper()

        return {"solution": solutions[answer_mapping[answer]]} 


"""

OPERATOR_OPTIMIZE_PROMPT = """
Your task is to optimize an Operator that executes within a SolveGraph to collaboratively address {type} problems.

When optimizing, you should preserve the original function of the Operator, focusing on enhancement rather than complete reconstruct.

Given an example SolveGraph or the current SolveGraph, along with the Operator description and its corresponding prompt, please execute the Operator within the SolveGraph, refining the prompt to improve performance. Remember, in the solvengraph you can only use the current operator.

In your response, make only one modification (e.g., a single sentence) and provide the updated Operator_description, Prompt, and SolveGraph enclosed within XML tags. These will be used as the new Prompt for the Operator in subsequent computations and iterations. Ensure that your modifications are complete and accurate to prevent any potential runtime errors.

Ensure the SolveGraph output is formatted correctly so that it can be directly used in code execution. Ensure that each prompt 's placeholder is consistent with SolveGraph.
"""


# TODO 这里的输入可能还要看一下graph的代码吧，不然不是很好弄；同时对应的Operator的参数也不是很好配置，这些最好都要成为优化的一部分
OPERATOR_OPTIMIZE_INPUT_PROMPT = """
Below is an operator and its corresponding solevgraph, prompt that demonstrated exceptional performance in a previous iteration (maximum score is 1, ):

<sample>
    <experience>{experience}</experience>
    <score>{score}</score>
    <solvegraph>{solvegraph}</solvegraph>
    <operator_description>{operator_description}</operator_description>
    <prompt>{prompt}</prompt>
</sample>
"""

OPERATOR_OPTIMIZE_GRAPH_EXAMPLE = """from typing import Literal
from examples.ags.w_action_node.optimized.Gsm8K.operators.{operator_name}.round_{round}.operator import *
from examples.ags.w_action_node.optimized.Gsm8K.operators.{operator_name}.round_{round}.prompt import *
from examples.ags.w_action_node.optimized.Gsm8K.operators.template.operator import Format, Generate
from metagpt.provider.llm_provider_registry import create_llm_instance
from metagpt.utils.cost_manager import CostManager

DatasetType = Literal["HumanEval", "MMBP", "Gsm8K", "MATH", "HotpotQa", "MMLU"]

{graph}

                    """


GRAPH_OPTIMIZE_PROMPT = """You are building a Graph and corresponding Prompt to jointly solve {type} problems. 
Referring to the given graph and prompt, which forms a basic example of a {type} solution approach, 
please reconstruct and optimize them. You can add, modify, or delete nodes, parameters, or prompts. Include your 
single modification in XML tags in your reply. Ensure they are complete and correct to avoid runtime failures. When 
optimizing, you can incorporate critical thinking methods like Review, Revise, Ensemble, selfAsk, etc. Consider 
Python's loops (for, while, list comprehensions), conditional statements (if-elif-else, ternary operators), 
or machine learning techniques (e.g., linear regression, decision trees, neural networks, clustering). The graph 
complexity should not exceed 10. Use logical and control flow (IF-ELSE, loops) for a more enhanced graphical 
representation.Ensure that all the prompts required by the current graph from prompt_custom are included.Exclude any other prompts.
Output the modified graph and all the necessary Prompts in prompt_custom (if needed)."""

GRAPH_INPUT = """
Here is a Graph and corresponding Prompt(only relate to the Custom method) that performed excellently in a previous iteration (maximum score is 1):\n
<sample>
    <experience>{experience}</experience>
    <modification>None</modification>
    <score>{score}</score>
    <graph>{graph}</graph>
    <prompt>{prompt}</prompt>(only prompt_custom)
    <operator_description>{operator_description}</operator_description>
    <prompt_lib>{prompt_lib}</prompt_lib>(only prompt_lib description)
</sample>
First provide optimization ideas. Only add/modify/delete one detail point, extensive modifications are prohibited.\n\n
"""

GRAPH_CUSTOM_USE = """Here's an example of using the `custom` method in graph:
```
# You can write your own prompt in <prompt>prompt_custom</prompt> and then use it in the Custom method in the graph
response = await self.custom(input=problem, instruction=prompt_custom.XXX_PROMPT)
# You can also use an existing prompt from prompt_lib without writing your own
# response = await self.custom(input=problem, instruction=prompt_lib.XXX_PROMPT)
# The output from the Custom method can be placed anywhere you need it, as shown in the example below
solution = await self.generate(problem=problem + response['response'])
```
"""

GRAPH_TEMPLATE = """from typing import Literal
import examples.ags.w_action_node.optimized.{dataset}.graphs.template.operator as operator
import examples.ags.w_action_node.optimized.{dataset}.graphs.round_{round}.prompt as prompt_custom
import examples.ags.w_action_node.optimized.{dataset}.graphs.template.prompt_library as prompt_lib
from metagpt.provider.llm_provider_registry import create_llm_instance
from metagpt.utils.cost_manager import CostManager

DatasetType = Literal["HumanEval", "MMBP", "Gsm8K", "MATH", "HotpotQa", "MMLU"]

{graph}
                    """




OPERATOR_TEMPLATE = """from typing import Literal, List, Dict
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt

from metagpt.llm import LLM
from metagpt.provider.llm_provider_registry import create_llm_instance
from examples.ags.w_action_node.operator import Operator
from metagpt.actions.action_node import ActionNode
from examples.ags.w_action_node.optimized.Gsm8K.operators.template.operator_an import *
from examples.ags.w_action_node.optimized.Gsm8K.operators.{operator_name}.round_{round_number}.prompt import *

{operator}
                    """
