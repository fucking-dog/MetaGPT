IMAGE_DATA_EXTRACT_PROMPT = """
讲解这个图片的内容，并抽取出图片中的数据
"""

KEYWORD_EXTRACT_PROMPT = """
Extract the keywords from the data: 
data: {data}
"""

TEXT_GENERATE_PROMPT = """
Generate a text from the keywords, a fluent and concise text, can be used as a plot description: 
keywords: {keywords}
"""

TYPE_ANALYZE_PROMPT = """
Analyze the visualization type of the keywords, visualization type can be like bar chart, line chart, pie chart, etc.
keywords: {keywords}
"""

VISUALIZE_MAPPING_PROMPT = """
Generate the keywords use for visualization, the type of the keywords is visualization type, the plot is visualization data: 
visualization data: {data}
visualization type: {type}
"""
