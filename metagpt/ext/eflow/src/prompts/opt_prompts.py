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

# TODO Both Low 应该给一个正确答案？


WORKFLOW_OPTIMIZE_PROMPT = """
You are building a workflow and corresponding Prompt to jointly solve {type} problems. 

Referring to the given workflow and prompt, which forms a basic example of a {type} solution approach, 
please reconstruct and optimize them. 

You can add, modify, or delete nodes, parameters, or prompts. 
Include your single modification in XML tags in your reply. 
Ensure they are complete and correct to avoid runtime failures. 

When optimizing, you can incorporate critical thinking methods like review, revise, ensemble (generating multiple answers through different/similar prompts, then voting/integrating/checking the majority to obtain a final answer), selfAsk, etc. Consider 
Python's loops (for, while, list comprehensions), conditional statements (if-elif-else, ternary operators), or machine learning techniques (e.g., linear regression, decision trees, neural networks, clustering). 
The workflow complexity should not exceed 10. 

Use logical and control flow (IF-ELSE, loops) for a more enhanced graphical representation.
Ensure that all the prompts required by the current graph from prompt_custom are included.
Exclude any other prompts.
Output the modified graph and all the necessary Prompts in prompt_custom (if needed).
The prompt you need to generate is only the one used in `prompt_custom.XXX` within Custom. 
Other methods already have built-in prompts and are prohibited from being generated. 
Only generate those needed for use in `prompt_custom`; please remove any unused prompts in prompt_custom.
The generated prompt must not contain any placeholders.
Considering information loss, complex graphs may yield better results, but insufficient information transmission can omit the solution. 
It's crucial to include necessary context during the process.
"""