import pandas as pd
import json
import asyncio

from metagpt.ext.eflow.src.optimizer import Attributor
from metagpt.logs import logger

test_attribute_model = "gpt-4o-mini"
test_score_threshold = 0.5
dataset = "HumanEval"

test_attributor = Attributor(dataset, test_attribute_model, test_score_threshold)

test_dataset_path = "metagpt/ext/aflow/data/humaneval_incremental.jsonl"
raw_workflow_data_path = "raw_workflow_data.csv"
opt_workflow_data_path = "opt_workflow_data.csv"

raw_workflow = """
GENERATE_PROMPT = "{{problem}}\nGenerate an answer to this question, without any additional test cases. "
REFLECTION_ON_PUBLIC_TEST_PROMPT = "
Given a code problem and a python code solution which failed to pass test or execute, you need to analyze the reason for the failure and propose a better code solution.: 
### problem
{{problem}}

### Code Solution
{{solution}}

### Execution Result
{{exec_pass}}

#### Failed Test Case
{{test_fail}}

Please provide a reflection on the failed test cases and code solution, followed by a better code solution without any additional text or test cases.
"

    async def __call__(self, problem: str, entry_point: str):
        solution = await self.code_generate(problem, entry_point)
        test_result = await self.test(problem=problem, solution=solution['solution'], entry_point=entry_point)
        
        if test_result['result']:
            return test_result['solution'], self.get_cost()
        else:
            # If the test fails, try to generate a new solution with MOA
            problem = problem + "\n" + IMPROVE_CODE_PROMPT
            new_solution = await self.code_generate(problem, entry_point)
            return new_solution['solution'], self.get_cost()
"""

opt_workflow = """
GENERATE_PROMPT = "{{problem}}\nGenerate an answer to this question, without any additional test cases. "
REFLECTION_ON_PUBLIC_TEST_PROMPT = "
Given a code problem and a python code solution which failed to pass test or execute, you need to analyze the reason for the failure and propose a better code solution.: 
### problem
{{problem}}

### Code Solution
{{solution}}

### Execution Result
{{exec_pass}}

#### Failed Test Case
{{test_fail}}

Please provide a reflection on the failed test cases and code solution, followed by a better code solution without any additional text or test cases.
"
    async def __call__(self, problem: str, entry_point: str):
        solution = await self.code_generate(problem, entry_point)
        test_result = await self.test(problem=problem, solution=solution['solution'], entry_point=entry_point)
        
        for _ in range(3):
            if test_result['result']:
                return test_result['solution'], self.get_cost()
            
            problem = problem + "\n" + IMPROVE_CODE_PROMPT
            new_solution = await self.code_generate(problem, entry_point)
            test_result = await self.test(problem=problem, solution=new_solution['solution'], entry_point=entry_point)
        
        if test_result['result']:
            return test_result['solution'], self.get_cost()
        return new_solution['solution'], self.get_cost()

"""

def load_case_table(path, workflow):
    case_table = {}
    case_table["workflow"] = workflow
    case_table["cases"] = {}
    

    df = pd.read_csv(path)
    
    for _, row in df.iterrows():
        case_id = str(row['id'])
        case_table["cases"][case_id] = {
            "question": row['inputs'],
            "answer": row['prediction'], 
            "score": row['score']
        }

    return case_table




if __name__ == "__main__":

    async def main(raw_case_table, opt_case_table):
        attribute_table, cost = await test_attributor.attribute(raw_case_table, opt_case_table)
        logger.info(json.dumps(attribute_table, indent=4))
        logger.info(cost)

    raw_case_table = load_case_table(raw_workflow_data_path, raw_workflow)
    opt_case_table = load_case_table(opt_workflow_data_path, opt_workflow)

    asyncio.run(main(raw_case_table, opt_case_table))
