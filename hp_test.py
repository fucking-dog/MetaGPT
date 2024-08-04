import asyncio

from examples.ags.benchmark.hotpotqa import sample_generate, samples_generate

asyncio.run(samples_generate(mode='llm', result_path="samples.jsonl")) 
# asyncio.run(sample_generate(0, result_path="test.jsonl", mode="llm"))