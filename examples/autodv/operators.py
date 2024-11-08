from examples.autodv.operator_an import (
    ImageDataOp,
    KeywordOp,
    TextGenerateOp,
    TypeAnalyzeOp,
    VisualizeOp,
)
from examples.autodv.prompts import (
    IMAGE_DATA_EXTRACT_PROMPT,
    KEYWORD_EXTRACT_PROMPT,
    TEXT_GENERATE_PROMPT,
    TYPE_ANALYZE_PROMPT,
    VISUALIZE_MAPPING_PROMPT,
)
from metagpt.ext.aflow.scripts.operator import Operator
from metagpt.llm import LLM


# Stage 1: Image Data Extract
class ImageDataExtract(Operator):
    def __init__(self, llm: LLM, name: str = "ImageDataExtract"):
        super().__init__(llm, name)

    async def __call__(self, images: list[str]):
        prompt = IMAGE_DATA_EXTRACT_PROMPT.format(image_path=images)
        data = await self._fill_node(ImageDataOp, prompt, mode="single_fill", images=images)
        return data


# Stage 2: Keyword Extract
class Keyword(Operator):
    def __init__(self, llm: LLM, name: str = "Keyword"):
        super().__init__(llm, name)

    async def __call__(self, data: str):
        prompt = KEYWORD_EXTRACT_PROMPT.format(data=data)
        keywords = await self._fill_node(KeywordOp, prompt, mode="single_fill")
        return keywords


# Stage 3: Text Generate
class TextGenerate(Operator):
    def __init__(self, llm: LLM, name: str = "TextGenerate"):
        super().__init__(llm, name)

    async def __call__(self, keywords: str):
        prompt = TEXT_GENERATE_PROMPT.format(keywords=keywords)
        plot = await self._fill_node(TextGenerateOp, prompt, mode="single_fill")
        return plot


# Stage 4: Visualization, step 1: type analyze
class TypeAnalyze(Operator):
    def __init__(self, llm: LLM, name: str = "TypeAnalyze"):
        super().__init__(llm, name)

    async def __call__(self, keywords: str):
        prompt = TYPE_ANALYZE_PROMPT.format(keywords=keywords)
        visualize_type = await self._fill_node(TypeAnalyzeOp, prompt, mode="single_fill")
        return visualize_type


# step 2: visualize mapping
class VisualizeMapping(Operator):
    def __init__(self, llm: LLM, name: str = "VisualizeMapping"):
        super().__init__(llm, name)

    async def __call__(self, data: str, visualize_type: str):
        prompt = VISUALIZE_MAPPING_PROMPT.format(data=data, type=visualize_type)
        response = await self._fill_node(VisualizeOp, prompt, mode="xml_fill")
        return response
