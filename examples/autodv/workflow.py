from pathlib import Path

from examples.autodv.operators import (
    ImageDataExtract,
    Keyword,
    TextGenerate,
    TypeAnalyze,
    VisualizeMapping,
)
from metagpt.ext.aflow.scripts.workflow import Workflow
from metagpt.utils.common import encode_image


class AutoDVWorkflow(Workflow):
    def __init__(
        self,
        name: str = "AutoDV",
        llm_config=None,
        dataset=None,
    ) -> None:
        super().__init__(name, llm_config, dataset)

        # 初始化所有operators
        self.image_data_extractor = ImageDataExtract(self.llm)
        self.keyword_extractor = Keyword(self.llm)
        self.text_generator = TextGenerate(self.llm)
        self.type_analyzer = TypeAnalyze(self.llm)
        self.visualizer = VisualizeMapping(self.llm)

    async def __call__(self, images: list[str]):
        """执行自动数据可视化的完整工作流程

        Args:
            images: 输入图片路径列表

        Returns:
            tuple: (plot_text, visualization_result) - 生成的描述文本和可视化结果
        """
        # invoice_path = Path(__file__).parent.joinpath("..", "tests", "data", "invoices", "invoice-2.png")

        images_b64 = [encode_image(Path(image)) for image in images]
        # Stage 1: 从图片提取数据
        image_data = await self.image_data_extractor(images_b64)

        # Stage 2: 提取关键词
        keywords = await self.keyword_extractor(image_data)

        # Stage 3: 生成描述文本
        plot = await self.text_generator(keywords)

        # Stage 4: 可视化分析
        # Step 1: 分析可视化类型
        visualize_type = await self.type_analyzer(keywords)

        # Step 2: 生成可视化映射
        visualization_result = await self.visualizer(keywords, visualize_type)

        return plot, visualization_result
