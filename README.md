
# 方法介绍

![img.png](result/img.png)



# 运行过程

- 准备问题题库，存为JSON文件，放到math_ai/dataset文件夹下。JSON文件的格式如下

  ~~~json
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

​		 如需复现，我们将可以提供处理好的JSON题目。

- 按照 Meta-README.md --> Get Started 中的指示，配置metagpt运行环境
- 模型为openai gpt-4-turbo，将模型相关参数填充在如下两个地方
  - 根据Meta-README.md --> Get Started --> Configuration中的指示，在~/.metagpt/config2.yaml中填充api_type、model、base_url、api_key等等
  - 在math_ai/codebase/engine/llm.py中，填充自己的base_url和api_key

- 在run.py中填入题库的json路径，运行run.py文件，等待运行结果。每道题大约需要5分钟，花费1-2$。
- 运行的结果放在result文件夹中。在比赛过程中，会多次重复上述过程，为每道题生成大约10道候选答案，再从中选择合适的答案进行提交。
- 由于电脑环境不同，如在复现的过程中遇到任何问题，都可以联系我们进行解决！

