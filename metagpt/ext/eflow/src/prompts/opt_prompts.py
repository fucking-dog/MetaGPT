ATTRIBUTE_ON_RAW_BETTER_PROMPT = """
## Instruction
Given a question, and two workflows with corresponding answers. The raw workflow is better than the optimized workflow for this question.
Your task is to attribute why the raw workflow is better than the optimized workflow.

Specifically, you should attribute from two aspects:
1. why the optimized answer is not correct when compared with the raw answer.
2. which part of optimized workflow's maybe result in this error.

Please remember that the answer is the execution result of the Workflow, and the analysis of the Workflow is actually the analysis of the Workflow's logic.

## Input
Raw workflow:
{raw_workflow}

Raw answer:
{raw_answer}

Optimized workflow:
{opt_workflow}

Optimized answer:
{opt_answer}

## Output Format
When output, you need to output your thought and attribution within XML Tag. In the "thought" field, provide a detailed explanation of your thought process.  In the "attribution_on_answer" field, output your attribution on the answer to the question in one senetence. In the "attribution_on_workflow" field, output your attribution on the workflow to the question in one senetence.
"""


ATTRIBUTE_ON_OPT_BETTER_PROMPT = """
## Instruction
Given a question, and two workflows with corresponding answers. The optimized workflow is better than the raw workflow for this question.
Your task is to attribute why the optimized workflow is better than the raw workflow.

Specifically, you should attribute from two aspects:
1. why the optimized answer is more accurate or efficient compared to the raw answer.
2. which steps in the optimized workflow lead to this improvement.

## Input
Raw workflow:
{raw_workflow}

Raw answer:
{raw_answer}

Optimized workflow:
{opt_workflow}

Optimized answer:
{opt_answer}

## Output Format
When output, you need to output your thought and attribution within XML Tag. In the "thought" field, provide a detailed explanation of your thought process.  In the "attribution_on_answer" field, output your attribution on the answer to the question in one senetence. In the "attribution_on_workflow" field, output your attribution on the workflow to the question in one senetence.
"""

ATTRIBUTE_ON_BOTH_LOW_PROMPT = """
## Instruction
Given a question, and two workflows with corresponding answers. Both workflows provide unsatisfactory answers.
Your task is to attribute why both workflows failed to provide good answers.

Specifically, you should attribute from two aspects:
1. what are the common issues in both workflows that lead to poor results.
2. what's the common reason for the failure of both two workflows.

## Input
Raw workflow:
{raw_workflow}

Raw answer:
{raw_answer}

Optimized workflow:
{opt_workflow}

Optimized answer:
{opt_answer}

## Output Format
When output, you need to output your thought and attribution within XML Tag. In the "thought" field, provide a detailed explanation of your thought process.  In the "attribution_on_answer" field, output your attribution on the answer to the question in one senetence. In the "attribution_on_workflow" field, output your attribution on the workflow to the question in one senetence.
"""


ATTRIBUTE_OVERALL_PROMPT = """
## Instruction
Given a dataset about {field} questions, a workflow, and attribution conclusions from analyzing this workflow's performance on various questions in the dataset. 
Your task is to summarize these attributions to form a comprehensive evaluation of the workflow's strengths, weaknesses, and potential improvements.

The attribution conclusions are mainly categorized into three types:
1. Reasons why this workflow performs better than previous workflows
2. Reasons why this workflow performs worse than previous workflows
3. Common issues identified across the current workflow that require evolution, based on answer analysis

## Input
Workflow:
{workflow}

Attribution List:
{attribution_list}

## Output Format
When output, you need to output your thought and attribution within XML Tag:
In the "thought" field: Provide a detailed explanation of your analysis process
In the "strengths" field: Summarize the advantages and strong points of this workflow
In the "weaknesses" field: Summarize the disadvantages and limitations of this workflow
In the "improvements" field: Suggest potential directions for improving this workflow
"""

WORKFLOW_OPTIMIZE_PROMPT = """
You are buidling a workflow to solve {question_type} problems.
Given a workflow and corresponding prompt, which is a workflow that can run on {question_type} problems. 
Also, you are given the strengths, weaknesses, and potential improvements of this workflow.
Your task is to optimize the workflow to make it better.

## Optimization Rules
1. You can add, modify, or delete nodes, opeartors, or prompts in the workflow.
2. And in each optimization round, you can only make one modification. Make sure the optimized workflow and prompt are complete and correct to avoid runtime failure.
3. Ensure that all the prompts required by the current workflow from prompt_custom are included, and exclude any other prompts.
4. Output the modified workflow and all the necessary Prompts in prompt_custom (if needed).
5. The prompt you need to generate is only the one used in `prompt_custom.XXX` within Custom. 
6. Other methods already have built-in prompts and are prohibited from being generated. 
7. Only generate those needed for use in `prompt_custom`; please remove any unused prompts in prompt_custom.
8. The generated prompt must not contain any placeholders.
9. Considering information loss, complex workflows may yield better results, but insufficient information transmission can omit the solution.
10. It's crucial to include necessary context during the process. 
"""



WORKFLOW_CUSTOM_USE = """\nHere's an example of using the `custom` method in workflow:
```
# You can write your own prompt in <prompt>prompt_custom</prompt> and then use it in the Custom method in the workflow
response = await self.custom(input=problem, instruction=prompt_custom.XXX_PROMPT)
# You can also concatenate previously generated string results in the input to provide more comprehensive contextual information.
# response = await self.custom(input=problem+f"xxx:{{xxx}}, xxx:{{xxx}}", instruction=prompt_custom.XXX_PROMPT)
# The output from the Custom method can be placed anywhere you need it, as shown in the example below
solution = await self.generate(problem=f"question:{{problem}}, xxx:{response['response']}")
```
Note: In custom, the input and instruction are directly concatenated(instruction+input), and placeholders are not supported. Please ensure to add comments and handle the concatenation externally.\n

**Introducing multiple operators at appropriate points can enhance performance. If you find that some provided operators are not yet used in the workflow, try incorporating them.**
"""

WORKFLOW_INPUT = """
Here is a workflow and the corresponding prompt (prompt only related to the custom method) that performed excellently in a previous iteration. 
You must make further optimizations and improvements based on this workflow. 
The modified workflow must differ from the provided example, and the specific differences should be noted within the <modification>xxx</modification> section.\n

<sample>
    <optimization_signals>{optimization_signals}</optimization_signals>
    <modification>(such as:add /delete /modify/ ...)</modification>
    <workflow>{workflow}</workflow>
    <prompt>{prompt}</prompt>(only prompt_custom)
    <operator_description>{operator_description}</operator_description>
</sample>


First, provide optimization ideas. 
**Only one detail point can be modified at a time**, and no more than 5 lines of code may be changed per modification—extensive modifications are strictly prohibited to maintain project focus!
When introducing new functionalities in the workflow, please make sure to import the necessary libraries or modules yourself, except for operator, prompt_custom, create_llm_instance, and CostManage, which have already been automatically imported.
**Under no circumstances should workflow output None for any field.**
Use custom methods to restrict your output format, rather than using code (outside of the code, the system will extract answers based on certain rules and score them).
It is very important to format the workflow output answers, you can refer to the standard answer format in the log.
"""