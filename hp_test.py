import asyncio

from examples.ags.benchmark.hotpotqa import sample_generate, samples_generate, eval

path = "samples_1000_sup_unique.jsonl"
# asyncio.run(samples_generate("llm", "hotpotqa_1000.jsonl", path))
for i in [528, 707, 582, 967, 974, 849, 722, 725, 726, 599, 854, 984, 994, 745, 753, 881, 758, 759, 767]:
    asyncio.run(sample_generate(i, path, "llm"))

eval_path = path[:-6] + "eval.jsonl"  
eval(path, "hotpotqa_1000.jsonl", eval_path)