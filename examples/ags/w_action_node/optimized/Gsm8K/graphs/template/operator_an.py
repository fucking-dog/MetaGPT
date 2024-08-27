from pydantic import BaseModel, Field


class GenerateOp(BaseModel):
    content: str = Field(default="", description="Your response")


class FormatOp(BaseModel):
    content: str = Field(default="", description="Formated answer")