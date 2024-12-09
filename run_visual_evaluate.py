import asyncio
from metagpt.ext.aflow.benchmark.matplotbench import VisualizationCompare
from metagpt.provider.llm_provider_registry import create_llm_instance
from metagpt.configs.models_config import ModelsConfig
from metagpt.utils.common import encode_image
from pathlib import Path

generated_image = "metagpt/ext/eflow/code_space/matplotbench/4/4.png"
ground_truth = "metagpt/ext/aflow/data/matplotbench_data/ground_truth/example_6.png"

# llm as a judge 
llm_config = ModelsConfig.default().get("gpt-4o-mini")
model = create_llm_instance(llm_config)

async def main():
    visual_compare = VisualizationCompare(model)
    query = "Generate a nested pie plot using a bar plot method in polar coordinates. The plot should be based on a numerical array `data` with values [[80., 20.], [50., 50.], [40., 60.]]. Normalize this data to 2 pi. Use a colormap that provides a range of 20 colors to create two color arrays. Create two pie plots that are nested together with a blank center that is not filled in, the two rings should have the same thickness. The rings should have a white edge with line width of 1 to clearly delineate each segment, and they should be aligned at the edge of each bar segment for visual consistency. The outer pie plot should use the sum of the normalized data for the width and the inner pie plot should use the flattened normalized data for the width. Use outer_colors = cmap(np.arange(3)*4), inner_colors = cmap([1, 2, 5, 6, 9, 10]) to paint the nested pie chart. The title of the plot should be 'Pie plot with bar method and polar coordinates'. The axis should be turned off."
    score = await visual_compare(query, [generated_image, ground_truth])
    print(score)

if __name__ == "__main__":
    asyncio.run(main())

