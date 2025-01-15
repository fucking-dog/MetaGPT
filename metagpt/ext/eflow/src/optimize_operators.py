from metagpt.ext.eflow.src.abstract import Operator
from metagpt.ext.eflow.src.prompts.opt_prompts import ATTRIBUTE_ON_RAW_BETTER_PROMPT, ATTRIBUTE_ON_OPT_BETTER_PROMPT, ATTRIBUTE_ON_BOTH_LOW_PROMPT, ATTRIBUTE_OVERALL_PROMPT, WORKFLOW_OPTIMIZE_PROMPT
from metagpt.llm import LLM

class AttributeQueryOperator(Operator):
    def __init__(self, model: LLM):
        super().__init__(model, "Attribute")
        self.schema = [
            {"name": "thought", "type": "str", "description": "Your thought of the attribution process for this case"},
            {"name": "attribution_on_answer", "type": "str", "description": "The attribution of this case on the answer"},
            {"name": "attribution_on_workflow", "type": "str", "description": "The attribution of this case on the workflow"},
        ]

    async def __call__(self, raw_workflow, opt_workflow, question_description, raw_answer, opt_answer, mode: str, model: LLM = None):
        if mode == "raw_better":
            prompt = ATTRIBUTE_ON_RAW_BETTER_PROMPT.format(
                raw_workflow=raw_workflow, 
                opt_workflow=opt_workflow, 
                question_description=question_description, 
                raw_answer=raw_answer, 
                opt_answer=opt_answer
            )
        elif mode == "opt_better":  
            prompt = ATTRIBUTE_ON_OPT_BETTER_PROMPT.format(
                raw_workflow=raw_workflow, 
                opt_workflow=opt_workflow, 
                question_description=question_description, 
                raw_answer=raw_answer, 
                opt_answer=opt_answer
            )
        elif mode == "both_low":
            prompt = ATTRIBUTE_ON_BOTH_LOW_PROMPT.format(
                raw_workflow=raw_workflow, 
                opt_workflow=opt_workflow, 
                question_description=question_description, 
                raw_answer=raw_answer, 
                opt_answer=opt_answer
            )
        response = await self._fill_node(
            op_schema=self.schema, prompt=prompt, format="xml_fill", model=model, 
        )
        return response
    
class AttributeOverallOperator(Operator):
    def __init__(self, model: LLM):
        super().__init__(model, "AttributeOverall")
        self.schema = [
            {"name": "thought", "type": "str", "description": "Your thought of the attribution process for this case"},
            {"name": "strengths", "type": "str", "description": "The strengths of this workflow"},
            {"name": "weaknesses", "type": "str", "description": "The weaknesses of this workflow"},
            {"name": "improvements", "type": "str", "description": "Potential improvements of this workflow"},
        ]
    
    async def __call__(self, workflow, attribution_list, model: LLM = None):
        prompt = ATTRIBUTE_OVERALL_PROMPT.format(field="code generation", workflow=workflow, attribution_list=attribution_list)
        response = await self._fill_node(
            op_schema=self.schema, prompt=prompt, format="xml_fill", model=model, 
        )
        return response
    

class WorkflowOptimizeOperator(Operator):
    def __init__(self, model: LLM):
        super().__init__(model, "WorkflowOptimize")
        self.schema = [
            {"name": "modification", "type": "str", "description": "The modification of this workflow"},
            {"name": "workflow", "type": "str", "description": "The full implementation of the workflow"},
            {"name": "prompt", "type": "str", "description": "The prompt of the workflow"}, 
        ]

    async def __call__(self, optimize_signal, raw_workflow, custom_prompt, operator_description, model: LLM = None):
        """
        Version 1.0: 只考虑使用已有的优化信号，对raw_workflow进行优化
        """
        prompt = WORKFLOW_OPTIMIZE_PROMPT.format(
            optimize_signal=optimize_signal, 
            raw_workflow=raw_workflow, 
            custom_prompt=custom_prompt, 
            operator_description=operator_description
        )
        response = await self._fill_node(
            op_schema=self.schema, prompt=prompt, format="xml_fill", model=model, 
        )
        return response