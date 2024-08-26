from pydantic import BaseModel, Field


class GenerateOp(BaseModel):
    solution: str = Field(default="", description="Your solution for this problem")

