# 配置
1. 首先按照README.md文件，完成MetaGPT项目配置
2. 进入工作目录，在`math_ai/codebase/engine/llm.py` 中，配置`apikey`与`base_url`
3. 进入工作目录，进入`run.py`填入JSON文件路径，运行 `python run.py`

# JSON 题目文件
JSON 题目文件将由赛事组提供的LaTex格式赛题生成，如需复现，我们将在赛后提供处理好的JSON格式题目，或提供数据处理的程序。

在提交的代码方案中，我们使用历史赛题生成的JSON数据进行测试。