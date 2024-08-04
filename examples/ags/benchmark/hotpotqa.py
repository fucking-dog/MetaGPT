from typing import Literal, Optional
import asyncio
import json
import re
import string
import aiofiles

from metagpt.llm import LLM
from metagpt.logs import logger
# from examples.ags.w_action_node.graph import HotpotQAGraph
from examples.ags.w_action_node.operator import GenerateOnContext

def sort_json_by_key(input_path, output_path):
    with open(input_path) as f:
        data = [json.loads(line) for line in f]
    data.sort(key=lambda x: x["task_id"])
    with open(output_path, "w") as f:
        for line in data:
            f.write(json.dumps(line) + "\n")
    

generate_on_context = GenerateOnContext(llm=LLM())
# solver = HotpotQAGraph(name="solver", llm=LLM(), criteria="correctness, efficiency, readability", vote_count=5)

ModeType = Literal["ags", "alpha_codium", "llm"]

def get_hotpotqa(path: str = "hotpot.jsonl"):

    #Parses each jsonl line and yields it as a dictionary
    def parse_jsonl(path):
        with open(path) as f:
            for line in f:
                yield json.loads(line)
    
    datas = list(parse_jsonl(path))
    return {data["_id"]: data for data in datas}

async def llm_generate(id):
    dp = get_hotpotqa()[id]
    paragraphs = [item[1] for item in dp['context'] if isinstance(item[1], list)]
    context_str = "\n".join(" ".join(paragraph) for paragraph in paragraphs)

    answer_result = await generate_on_context(dp['question'], context_str)
    sample_dict = dict(task_id=id, answer=answer_result)
    return sample_dict

async def route_generate(mode: ModeType, id):
    if mode == "ags":
        pass
    elif mode == "llm":
        sample_dict = await llm_generate(id)
    else:
        raise ValueError(f"Invalid mode: {mode}")
    return sample_dict

async def sample_generate(id, result_path: str = "samples.jsonl", mode: ModeType = "llm"):
    sample_dict = await route_generate(mode, id)
    async with aiofiles.open(result_path, mode="a") as f:
        await f.write(json.dumps(sample_dict) + "\n")
    sort_json_by_key(result_path, result_path)

async def samples_generate(mode: ModeType, data_path: str = "hotpot.jsonl", result_path: str = "samples.jsonl"):
    ids = list(get_hotpotqa().keys())

    file_lock = asyncio.Lock()

    async def answer_and_write(mode: ModeType, id) -> Optional[str]:
        try:
            sample_dict = await route_generate(mode, id)
        except Exception:
            return id
        async with file_lock:
            async with aiofiles.open(result_path, mode="a") as f:
                await f.write(json.dumps(sample_dict) + "\n")
        return None

    tasks = [answer_and_write(mode, id) for id in ids]
    results = await asyncio.gather(*tasks)
    failed_ids = [id for id in results if id is not None]

    if failed_ids:
        logger.info(failed_ids)
        for id in failed_ids:
            try:
                await sample_generate(id, result_path, mode)
                failed_ids.remove(id)
            except Exception:
                logger.error(f"Failed to generate sample for id: {id}")

    sort_json_by_key(result_path, result_path)

    if not failed_ids:
        eval_path = result_path[:-6] + "_eval.json"
        logger.info(eval(result_path, data_path))

def normalize_answer(s):

    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def exact_match_score(prediction, ground_truth):
    return (normalize_answer(prediction) == normalize_answer(ground_truth))

async def eval(prediction_file, gold_file):
    sort_json_by_key(prediction_file, prediction_file)
    with open(prediction_file) as f:
        predictions = [json.loads(line) for line in f]

    with open(gold_file) as f:
        golds = [json.loads(line) for line in f]

    em = 0

    for prediction, gold in zip(predictions, golds):
        if(prediction["task_id"] != gold["_id"]):
            raise ValueError("Task IDs do not match")
        em += exact_match_score(prediction["answer"], gold["answer"])

    logger.info(f"EM: {em/len(predictions)}")
    
