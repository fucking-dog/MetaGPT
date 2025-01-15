from typing import Dict, List
from pydantic import BaseModel, Field, create_model
from metagpt.actions.action_node import ActionNode
from metagpt.configs.models_config import ModelsConfig
from metagpt.ext.aflow.scripts.evaluator import DatasetType
from metagpt.llm import LLM
from metagpt.provider.llm_provider_registry import create_llm_instance
from metagpt.utils.cost_manager import CostManager


class Schema(BaseModel):

    @classmethod
    def create(cls, attributes: List[Dict])-> BaseModel:
        field_definitions = {
            attr["name"]: (str, Field(
                default="",
                description=attr.get("description", ""),
                # 可以在这里添加更多字段配置
            ))
            for attr in attributes
        }

        DynamicModel = create_model(
            "DynamicModel",
            __base__=cls,  # 使用 Schema 作为基类
            **field_definitions
        )
        
        return DynamicModel
    
    def __init__(self, **data):
        """
        初始化方法，处理模型实例的创建
        """
        super().__init__(**data)


class Operator:
    def __init__(self, model: LLM, name: str):
        self.default_model = model
        self.name = name

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    async def _fill_node(self, op_schema, prompt, format=None, model: LLM = None, **extra_kwargs):
        op_class = Schema.create(op_schema)
        fill_kwargs = {"context": prompt, "llm": model}
        if model is None:
            fill_kwargs["llm"] = self.default_model
        if format:
            fill_kwargs["mode"] = format

        fill_kwargs.update(extra_kwargs)
        node = await ActionNode.from_pydantic(op_class).fill(**fill_kwargs)
        return node.instruct_content.model_dump()


class Workflow:
    def __init__(
        self,
        name: str,
        llm_names: list,
        dataset: DatasetType,
    ) -> None:
        self.name = name
        self.dataset = dataset
        self.llm_dict = self.create_llms(llm_names)
    
    def save_reason_process(self):
        pass

    def get_cost(self):
        # 累计所有llm的cost
        total_cost = 0
        for llm in self.llm_dict.values():
            total_cost += llm.cost_manager.total_cost
        return total_cost

    def create_llms(self, llm_names: list):
        llm_dict = {}
        for llm_name in llm_names:
            llm_config = ModelsConfig.default().get(llm_name)
            llm_dict[llm_name] = create_llm_instance(llm_config)
            llm_dict[llm_name].cost_manager = CostManager()
        return llm_dict

    async def __call__(self, problem: str):
        """
        Implementation of the workflow
        """
        raise NotImplementedError("This method should be implemented by the subclass")
