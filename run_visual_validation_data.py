from metagpt.ext.eflow.src.abstract import Workflow
from metagpt.ext.eflow.src.operators import VisualFeedback, VisualizationProgrammer
import asyncio
# 1. Visual FeedBack
# 2. Code Generate (是否要与Programmer分开？)
# 3. Code Check

# 中间的Imgae都通过path来进行传递

class MatplotWorkflow(Workflow):
    def __init__(
            self,
            name: str,
            llm_names: list,
            dataset: str,
    ):
        super().__init__(name, llm_names, dataset)
        self.visual_feedback = VisualFeedback(self.llm_dict["gpt-4o-mini"])
        self.visualization_programmer = VisualizationProgrammer(self.llm_dict["gpt-4o-mini"])
    
    async def __call__(self, query:str, query_id:int, csv_path:str=None):
        save_image_path = f"metagpt/ext/eflow/code_space/matplotbench/{query_id}/{query_id}.png"
        if csv_path is None:
            csv_path = "No data need to be use."
        
        init_image_info = await self.visualization_programmer(query=query, file_path=save_image_path, csv_file=csv_path)
        visual_feedback = await self.visual_feedback(query=query, image_path=init_image_info["visualization_path"])
        final_image_info = await self.visualization_programmer(query=query, file_path=init_image_info["visualization_path"], analysis=visual_feedback, csv_file=csv_path)

        return final_image_info

if __name__ == "__main__":
    async def main():
        workflow = MatplotWorkflow(name="matplot", llm_names=["gpt-4o-mini"], dataset="matplotbench")
        query = "Generate a nested pie plot using a bar plot method in polar coordinates. The plot should be based on a numerical array `data` with values [[80., 20.], [50., 50.], [40., 60.]]. Normalize this data to 2 pi. Use a colormap that provides a range of 20 colors to create two color arrays. Create two pie plots that are nested together with a blank center that is not filled in, the two rings should have the same thickness. The rings should have a white edge with line width of 1 to clearly delineate each segment, and they should be aligned at the edge of each bar segment for visual consistency. The outer pie plot should use the sum of the normalized data for the width and the inner pie plot should use the flattened normalized data for the width. Use outer_colors = cmap(np.arange(3)*4), inner_colors = cmap([1, 2, 5, 6, 9, 10]) to paint the nested pie chart. The title of the plot should be 'Pie plot with bar method and polar coordinates'. The axis should be turned off."
        query_id = 4
        csv_path = None
        final_image = await workflow(query, query_id, csv_path)
        print(final_image)
    asyncio.run(main())


# chart visual feedback; code generate; code vs ground truth; human feedback; 

# Table + NL -> Chart
# Table + NL -> InfoGraphics(Diffusion Model)
# url/txt/PDF/article + NL -> Chart 
# url/txt/PDF/article + NL -> InfoGraphics(Diffusion Model)
# NL -> Chart（数据无关的Example）


# 1. 两类eval
# 2. 主流程：route function -> 5 * Workflow
# 3. 实际代码构建：Workflow 获得是通过搜索得到的，EFLOW 
# 4. 故事：为any to chart 构建了xxx种基础动作，你组织了五种有效的worklfow，并且，构建了route函数，通过这样的一个系统，实现了any2chart/vis