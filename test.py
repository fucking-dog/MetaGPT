from openai import OpenAI
client = OpenAI(api_key="sk-jXcmlo9TpZCpuLnxA80f4a3284Db48AbB874560d714f7446",base_url="https://api.aigcbest.top/v1/models")

print(client.models.list())
