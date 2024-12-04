from enum import Enum
from pathlib import Path
from typing import List

from pydantic import BaseModel

from examples.bflow.operators import AgenticOptimize
from metagpt.configs.llm_config import LLMConfig
from metagpt.configs.models_config import ModelsConfig
from metagpt.llm import LLM
from metagpt.provider.llm_provider_registry import create_llm_instance


class LLMProfile(BaseModel):
    name: str
    config: LLMConfig
    description: str
    cost: float
    max_tokens: int

    def _get_description(self):
        full_description = f"name: {self.name}, description: {self.description}, cost: {self.cost}/1000tokens, max_tokens: {self.max_tokens}"
        return full_description


class OptimizeObject(Enum):
    WORKFLOW = "workflow"
    PROMPT = "prompt"
    OPERATOR = "operator"


class OptimizeActionType(Enum):
    MODIFY = "modify"
    ADD = "add"
    DELETE = "delete"


class AgenticOptimizer:
    """
    第一版本，实现最基础的自主增删改查
    第二版本，实现基于过程经验的自主优化
    第三版本，实现基于过程经验与Case Study的自我优化
    第四版本，实现优化意图，能够自主选择LLM，基于query锁定一个或者多个目标优化
    第五版本，添加llm call 限制/cost 限制。
    第六版本，添加树状状态结构，能够实现roll back 动作，避免修改
    """

    def __init__(self, optimize_llm_config: LLMConfig, execute_llms: List[LLMProfile], optimized_path: str):
        self.optimize_llm_config = optimize_llm_config
        self.optimize_llm = create_llm_instance(self.optimize_llm_config)
        self.execute_llms = execute_llms
        self.agentic_optimize = AgenticOptimize(llm=self.optimize_llm)
        self.optimized_path = optimized_path
        print(type(self.agentic_optimize.llm))
        self.max_round = 30

    async def _optimize_workflow(self, workflow, prompts, operators):
        """基于当前workflow和operators进行优化

        Args:
            workflow (str): 当前的workflow代码
            operators (List): 可用的operators列表

        Returns:
            Dict: 包含优化后的workflow和修改说明
        """
        workflow_code = workflow
        operators_code = "\n".join([str(op) for op in operators])
        # 调用AgenticOptimize获取优化建议
        response = await self.agentic_optimize(workflow_code, prompts, operators_code)

        # 解析response中的优化建议
        target_obj = response.get("target_object")
        action_type = response.get("action_type")
        code_range = response.get("range")
        new_code = response.get("content", "")

        print(target_obj)

        # TODO 先只做workflow优化
        if target_obj.upper() == OptimizeObject.WORKFLOW.value:
            if action_type.upper() == OptimizeActionType.MODIFY.value:
                # 获取需要修改的代码行范围
                start_line, end_line = map(int, code_range.split("-"))
                workflow_lines = workflow.split("\n")

                # 替换指定范围的代码
                workflow_lines[start_line - 1 : end_line] = new_code.split("\n")
                modified_workflow = "\n".join(workflow_lines)

                return {"workflow": modified_workflow, "modification": f"Modified workflow lines {code_range}"}

            elif action_type.upper() == OptimizeActionType.ADD.value:
                # 在指定位置添加新代码
                insert_line = int(code_range)
                workflow_lines = workflow.split("\n")
                workflow_lines.insert(insert_line - 1, new_code)
                modified_workflow = "\n".join(workflow_lines)

                return {"workflow": modified_workflow, "modification": f"Added new code at line {insert_line}"}

            elif action_type.upper() == OptimizeActionType.DELETE.value:
                # 删除指定范围的代码
                start_line, end_line = map(int, code_range.split("-"))
                workflow_lines = workflow.split("\n")
                del workflow_lines[start_line - 1 : end_line]
                modified_workflow = "\n".join(workflow_lines)

                return {"workflow": modified_workflow, "modification": f"Deleted lines {code_range}"}
        elif target_obj.upper() == OptimizeObject.PROMPT.value:
            if action_type.upper() == OptimizeActionType.MODIFY.value:
                pass

        elif target_obj.upper() == OptimizeObject.OPERATOR.value:
            return "Operator optimization is not supported yet"

        return {"workflow": workflow, "modification": "No changes made"}

    async def optimize(self, dataset, initial_round: int, query: str = None):
        """执行优化流程

        Args:
            dataset: 用于评估的数据集
            initial_round (int): 初始轮次
            query (str, optional): 优化目标描述
        """

        # TODO
        # 1. 实现Operator的加载逻辑
        # 2. 加入线性的 Experience 设计
        # 3.
        current_round = initial_round

        while current_round < self.max_round:
            # 构建相关路径
            base_path = Path(self.optimized_path) / dataset / "workflows" / f"round_{current_round}"
            graph_path = base_path / "graph.py"
            prompt_path = base_path / "prompt.py"

            if not graph_path.exists():
                raise FileNotFoundError(f"Workflow file not found: {graph_path}")
            if not prompt_path.exists():
                raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

            # 加载当前轮次的文件
            with open(graph_path, "r") as f:
                self.workflow = f.read()
            with open(prompt_path, "r") as f:
                self.prompts = f.read()

            # 执行一轮优化
            result = await self._optimize_workflow(self.workflow, self.prompts, self.operators)

            # 更新workflow
            self.workflow = result["workflow"]

            # 保存优化后的文件
            next_round_path = Path(self.optimized_path) / dataset / "workflows" / f"round_{current_round + 1}"
            next_round_path.mkdir(parents=True, exist_ok=True)

            with open(next_round_path / "graph.py", "w") as f:
                f.write(self.workflow)
            with open(next_round_path / "prompt.py", "w") as f:
                f.write(self.prompts)

            # TODO: 实现评估逻辑
            # score = evaluate(self.workflow, dataset)

            current_round += 1


if __name__ == "__main__":
    claude_llm_config = ModelsConfig.default().get("claude-3-5-sonnet-20240620")
    mini_llm_config = ModelsConfig.default().get("gpt-4o-mini")
    optimizer = AgenticOptimizer(optimize_llm_config=claude_llm_config, execute_llms=[LLM(mini_llm_config)])

    mbpp_workflow = """
class Workflow:
    def __init__(
        self,
        name: str,
        llm_config,
        dataset: DatasetType,
    ) -> None:
        self.name = name
        self.dataset = dataset
        self.llm = create_llm_instance(llm_config)
        self.llm.cost_manager = CostManager()
        self.custom = operator.Custom(self.llm)
        self.custom_code_generate = operator.CustomCodeGenerate(self.llm)

    async def __call__(self, problem: str, entry_point: str):
        function_name_input = f"Problem: {problem}\nEntry Point: {entry_point}"
        function_name_result = await self.custom(input=function_name_input, instruction=prompt_custom.EXTRACT_FUNCTION_NAME_PROMPT)
        required_function_name = function_name_result['response']

        # Generate multiple solutions
        solutions = []
        for i in range(3):
            solution = await self.custom_code_generate(problem=problem, entry_point=entry_point, instruction=f"Use the function name: {required_function_name}")
            solutions.append(solution['response'])

        # Score and select the best solution
        score_input = f"Problem: {problem}\nEntry Point: {entry_point}\nSolutions:\n" + "\n".join(solutions)
        score_result = await self.custom(input=score_input, instruction=prompt_custom.SCORE_SOLUTIONS_PROMPT)
        best_solution = score_result['response']

        review_input = f"Problem: {problem}\nEntry Point: {entry_point}\nGenerated Solution:\n{best_solution}"
        review_result = await self.custom(input=review_input, instruction=prompt_custom.REVIEW_PROMPT)
        
        improved_solution = review_result['response'] if review_result['response'] else best_solution
        
        loop_check_input = f"Problem: {problem}\nEntry Point: {entry_point}\nImproved Solution:\n{improved_solution}"
        loop_check_result = await self.custom(input=loop_check_input, instruction=prompt_custom.INFINITE_LOOP_CHECK_PROMPT)
        
        loop_fixed_solution = loop_check_result['response'] if loop_check_result['response'] else improved_solution
        
        validate_input = f"Problem: {problem}\nEntry Point: {entry_point}\nRequired Function Name: {required_function_name}\nFinal Solution:\n{loop_fixed_solution}"
        validate_result = await self.custom(input=validate_input, instruction=prompt_custom.VALIDATE_FUNCTION_NAME_PROMPT)
        
        final_solution = validate_result['response'] if validate_result['response'] else loop_fixed_solution
        
        return final_solution, self.llm.cost_manager.total_cost
"""
    # 读取py文件中的所有内容，变成字符串
    with open(
        "/Users/trl/Github_project/MetaGPT-MathAI/metagpt/ext/aflow/scripts/optimized/MBPP/workflows/round_18/prompt.py",
        "r",
    ) as file:
        prompts = file.read()

    async def main():
        result = await optimizer._optimize_workflow(mbpp_workflow, prompts, [])
        print(result["workflow"])

    import asyncio

    asyncio.run(main())
