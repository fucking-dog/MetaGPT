from pydantic import BaseModel, Field


class ImageDataOp(BaseModel):
    data: str = Field(default="", description="The data extracted from the image")


class KeywordOp(BaseModel):
    keywords: str = Field(default="", description="The keywords extracted from the data")


class TextGenerateOp(BaseModel):
    plot: str = Field(default="", description="The plot generated from the prompt, discription of the prompt.")


class TypeAnalyzeOp(BaseModel):
    type: str = Field(default="", description="The type of visualization, e.g. bar chart, line chart, pie chart, etc.")


class VisualizeOp(BaseModel):
    data: str = Field(default="", description="The data use for visualization.")
    type: str = Field(default="", description="The type of visualization, e.g. bar chart, line chart, pie chart, etc.")
