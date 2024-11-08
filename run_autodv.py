import asyncio

from examples.autodv.workflow import AutoDVWorkflow
from metagpt.configs.models_config import ModelsConfig


async def main():
    four_o_mini_llm_config = ModelsConfig.default().get("gpt-4o-mini")
    workflow = AutoDVWorkflow(llm_config=four_o_mini_llm_config)

    # 执行完整工作流程
    plot, visualization_result = await workflow(["image.png"])

    print(plot)
    print("another line\n")
    print(visualization_result)


if __name__ == "__main__":
    asyncio.run(main())
