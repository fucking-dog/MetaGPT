# -*- coding: utf-8 -*-
# @Date    : 6/27/2024 19:46 PM
# @Author  : didi
# @Desc    : action nodes for operator

from pydantic import BaseModel, Field


class GenerateOp(BaseModel):
    response: str = Field(default="", description="Your solution for this problem")


class CodeGenerateOp(BaseModel):
    code: str = Field(default="", description="Your complete code solution for this problem")


class FormatOp(BaseModel):
    response: str = Field(default="", description="Your formatted answer for this problem")


class ReviewOp(BaseModel):
    review_result: bool = Field(
        default=False,
        description="The Review Result (Bool). If you think this solution looks good for you, return 'true'; If not, return 'false'.",
    )
    feedback: str = Field(
        default="None",  # 设置默认值为 None 表示字段是可选的
        description="Your feedback for this problem based on the criteria. This can be empty.",
    )


class ReviseOp(BaseModel):
    response: str = Field(default="", description="Based on the feedback, revised solution for this problem")


class FuEnsembleOp(BaseModel):
    final_solution: str = Field(default="", description="Output the final solution after analysis and integration")


class MdEnsembleOp(BaseModel):
    solution_letter: str = Field(default="", description="The letter of the chosen best solution (only one letter).")


class TestCaseExtractOp(BaseModel):
    test_cases: list = Field(
        default=[
            "assert candidate([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) == True",
            "assert candidate([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05) == False",
            "",
        ],
        description="Extracted test cases from the problem description",
    )


class RephraseOp(BaseModel):
    response: str = Field(default="", description="Rephrased problem description for this problem")


class ReflectionTestOp(BaseModel):
    reflection: str = Field(
        default="", description="Step-by-step reflection on code execution errors or test case failures"
    )
    refined_solution: str = Field(
        default="", description="Corrective solution for code execution errors or test case failures"
    )


class ScEnsembleOp(BaseModel):
    solution_letter: str = Field(default="", description="The letter of most consistent solution.")
