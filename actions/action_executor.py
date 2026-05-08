# -*- coding: utf-8 -*-
from tools.tool_registry import ToolRegistry
from runtime.execution_context import (
    ExecutionContext
)
from runtime.execution_state import (
    VariableResolver
)

class ActionExecutor(object):
    """根据schemas获取tool，并调用tool的run方法执行"""
    def __init__(self):
        self.tool_registry = ToolRegistry()
        self.execution_context = (
            ExecutionContext()
        )

    # --------------------------------
    # 执行Plan
    # --------------------------------
    def execute_plan(self, plan):
        results = []
        for action in plan.actions:
            result = self.execute_action(action)
            # 保存当前action执行后的返回值
            self.execution_context.add_result(
                result
            )
            # 更新Runtime Context，记录当前action所创建的节点路径
            self.update_context(result)
            results.append(result)
        return results

    # --------------------------------
    # 更新Runtime Context
    # --------------------------------
    def update_context(self, result):
        if not result:
            return
        node_path = result.get("node_path")
        if node_path:
            self.execution_context.set_last_created_node(
                node_path
            )

    # --------------------------------
    # 执行单个Action
    # --------------------------------
    def execute_action(self, action):
        tool = self.tool_registry.get_tool(
            action.tool
        )
        if tool is None:
            return {
                "success": False
            }
        # 动态解析变量
        args = VariableResolver.resolve_args(
            action.args,
            self.execution_context
        )
        result = tool.run(**args)
        return result