import pandas as pd
import json
import asyncio
from typing import List
from metagpt.ext.eflow.src.optimizer import Attributor, Optimizer
from metagpt.logs import logger

test_attribute_model = "gpt-4o-mini"
test_attribute_overall_model = "gpt-4o"
optimize_model = "claude-3-5-sonnet-20240620"
test_score_threshold = 0.5
dataset = "HumanEval"

def load_operators_description(operators: List[str]) -> str:
    path = f"op_desc.json"
    operators_description = ""
    for id, operator in enumerate(operators):
        operator_description = load_operator_description(id + 1, operator, path)
        operators_description += f"{operator_description}\n"
    return operators_description

def load_operator_description(id: int, operator_name: str, file_path: str) -> str:
    with open(file_path, "r") as f:
        operator_data = json.load(f)
        matched_data = operator_data[operator_name]
        desc = matched_data["description"]
        interface = matched_data["interface"]
        return f"{id}. {operator_name}: {desc}, with interface {interface})."


test_attributor = Attributor(dataset, test_attribute_model, test_attribute_overall_model, test_score_threshold)
operator_desc = load_operators_description(["CodeGenerate", "Test", "Custom", "CustomCodeGenerate", "ScEnsemble"])
test_optimizer = Optimizer(dataset=dataset, optimize_model=optimize_model, operator_description=operator_desc, root_path="")


test_dataset_path = "metagpt/ext/aflow/data/humaneval_incremental.jsonl"
raw_workflow_data_path = "raw_workflow_data.csv"
opt_workflow_data_path = "opt_workflow_data.csv"

raw_workflow = """
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
        opt_signal, attribute_cost, overall_cost = await test_attributor.attribute(raw_case_table, opt_case_table)
        logger.info(json.dumps(opt_signal, indent=4))
        logger.info(attribute_cost)
        logger.info(overall_cost)

        response = await test_optimizer.optimize_on_workflow_structure(workflow=opt_workflow, prompts="", optimize_signal=opt_signal)
        logger.info(json.dumps(response, indent=4))

    raw_case_table = load_case_table(raw_workflow_data_path, raw_workflow)
    opt_case_table = load_case_table(opt_workflow_data_path, opt_workflow)

    asyncio.run(main(raw_case_table, opt_case_table))
