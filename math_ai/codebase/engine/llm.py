# -*- coding: utf-8 -*-
# Date       : 2023/3/18
# Author     : Jiayi Zhang
# email      : didi4goooogle@gmail.com
# Description: LLM Class
import json
import time

import openai
from openai import OpenAI
from openai import AsyncClient

api_key = '<your api key>'
base_url = "<your base url>"

class OpenAILLM:
    def __init__(self, timeout=60):
        self.timeout = timeout
        self.api_key = api_key
        self.base_url = base_url
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self.async_client = AsyncClient(api_key=self.api_key, base_url=self.base_url)
        self.system_prompt = None

    def set_role(self, role: str):
        self.system_prompt = role

    def llm_response(self, prompt: str, model: str = "gpt-4-turbo", json_mode: bool = False, temperature: float = 0.7,
                     retries: int = 5):
        response_type = "text" if not json_mode else "json_object"
        messages = [{"role": "user", "content": prompt}] if self.system_prompt == None else [
            {"role": "system", "content": self.system_prompt}, {"role": "user", "content": prompt}]
        for i in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    response_format={"type": response_type}
                )
                usage = response.usage
                prompt_tokens = usage.prompt_tokens
                completion_tokens = usage.completion_tokens
                if json_mode:
                    result = response.choices[0].message.content
                    result = json.loads(result)
                else:
                    result = response.choices[0].message.content
                return result
            except openai.RateLimitError:
                print("Occur RateLimitError, sleep 20s")
                time.sleep(20)
                print("Rate limit retry")
            except Exception as e:
                print(f"{__name__} occurs: {e}")


if __name__ == "__main__":
    llm = OpenAILLM()
    print(llm.llm_response(prompt="Hello"))
