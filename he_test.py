import asyncio
from metagpt.llm import LLM
from examples.ags.benchmark.humaneval import sample_generate, samples_generate, extract_failure_tests, automatic_evalplus
from examples.ags.w_action_node.utils import jsonl_ranker

# 132 141 136 80 73
asyncio.run(sample_generate('HumanEval/45', result_path="4oaligned_llm1.jsonl",mode="llm"))
# asyncio.run(samples_generate(mode='llm',result_path="4oaligned_llm5.jsonl"))
# jsonl_ranker("samples.jsonl", "samples.jsonl")

# result_path = "3-sanitized.jsonl"
# if automatic_evalplus(result_path):
#     unpassed_exapmle = extract_failure_tests(result_path[:-6]+"_eval_results.json")
#     print(unpassed_exapmle)

# unpassed_exapmle = extract_failure_tests(file_path="2_eval_results.json")
# print(unpassed_exapmle)

# for example in failure_list:
#     asyncio.run(sample_generate(example))