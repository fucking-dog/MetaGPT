# Math AI
- 团队名称：SuperCarryMan

- 联系方式：<2020201387, 2020201526, 2020201597>@ruc.edu.cn

## 方法介绍

MetaGPT团队最新推出的DataInterpreter框架，以其独特的代码建模方法，为数据科学和数学问题的解决开辟了新途径。然而，这种纯粹依赖于代码建模的解决方案，可能会因缺乏深入的反思和验证过程而导致逻辑上的疏漏。正是基于对这一潜在缺陷的深刻认识，团队进一步开发了Math AI框架，旨在通过综合运用`inference（推理）`、`logic_validate（逻辑验证）`和`data_interpreter（数据解释）`三种高效的推理手段，对复杂的数学问题进行细致的拆解，并针对每个子问题选择合适的逻辑处理阶段，确保形成一个周密、经过多重验证的推理链条。

`MathAI`框架的推理阶段具体如下：

`inference`阶段：适用于那些不需要复杂代码建模和精确计算，而是更依赖于逻辑推理的子问题。
`logic_validate`阶段：适用于需要对已有推理进行逻辑验证，确保推理过程的合理性和正确性的子问题。
`data_interpreter`阶段：适用于那些需要精确的代码建模和计算，而简单的逻辑推理可能不足以解决问题的复杂子问题。
为了将这一推理链条转化为人类可读的形式，`MathAI`框架特别引入了润色代理，它能够将推理过程整合并以LaTeX格式呈现，使得最终的解答既准确无误，又易于理解。

Math AI框架的工作流程可以通过以下图表进行直观展示：

![img.png](result/mathai.png)

所有的prompt可以在`math_ai/codebase/prompt.py`中找到
## 运行过程

1. 准备问题题库，存为JSON文件，放到 `math_ai/dataset` 文件夹下。JSON文件的格式如下

   ~~~
   {
       '1':{
           'description':'', // 题干内容，从下发的题目文件中抽取得到，编写格式为markdown格式
           'type':'',        // 题目类型。分为简答题 证明题 选择题，有课题目可能涉及两个题型
       },
       '2':{
           'description':'', 
           'type':'',        
       },
       ......
   }
   ~~~

​		 如需复现，我们可以提供处理好的JSON题目。

2. 按照 `Meta_README.md -> Get Started` 中的指示，配置metagpt运行环境

3. 将模型相关参数填充在如下两个地方

   - 根据`Meta_README.md -> Get Started -> Configuration`中的指示，在`~/.metagpt/config2.yaml` 中填充api_type、model、base_url、api_key等等

   - 在 `math_ai/codebase/engine/llm.py` 中，填充自己的base_url和api_key

   在比赛中，我们的模型用的是openai gpt-4-turbo，

4. 在 `run.py` 中填入题库的JSON文件路径，运行 `run.py` 文件，等待运行结果。每道题大约需要5分钟，花费1-2$。

5. 将每道题的运行结果放在 `result` 文件夹中的txt文件。如果遇到乱码问题，请用gbk重新编码。

   在比赛过程中，我们会多次重复上述的答案生成过程，为每道题生成大约10道候选答案，再从中选择合适的答案进行提交。

---

​	NOTE:由于电脑环境不同，如在复现的过程中遇到任何问题，都可以联系我们进行解决！

---

