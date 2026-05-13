# -*- coding: utf-8 -*-
import json
import logging

from langchain_core.messages import SystemMessage, HumanMessage
from llm.tongyi_client import create_tongyi_llm
from actions.schemas import Action
from actions.plan import Plan
from tools.tool_registry import ToolRegistry

class TongyiAgent(object):
    def __init__(self):
        self.llm = create_tongyi_llm()
        self.tool_registry = ToolRegistry()

    def stream_plan_text(self, text, context):
        messages = [
            SystemMessage(content=self.build_system_prompt()),
            HumanMessage(content=self.build_user_prompt(text, context))
        ]
        for chunk in self.llm.stream(messages):
            content = getattr(chunk, "content", "")
            if content:
                yield content

    def run(self, text, context):
        messages = [
            SystemMessage(content=self.build_system_prompt()),
            HumanMessage(content=self.build_user_prompt(text, context))
        ]
        response = self.llm.invoke(messages)
        content = response.content
        print("=" * 50)
        print("LLM Raw Response:")
        print(content)
        plan_data = self.parse_json(content)
        if not plan_data:
            return None
        return self.build_plan(plan_data)
    def build_system_prompt(self):
        tool_text = self.tool_registry.get_prompt_text()
        print("----------------tool_text--------------")
        print(tool_text)
        print("\n")
        return f"""
你是一个 Houdini Agent Planner。

你的任务是根据用户请求和当前 Houdini 场景上下文，生成 JSON 执行计划。

你不能写 Python 代码。
你不能直接调用 hou API。
你只能从下面的工具列表中选择工具。

可用工具如下：

{tool_text}

输出格式必须是 JSON：

{{
  "actions": [
    {{
      "tool": "工具名",
      "args": {{
        "参数名": "参数值"
      }},
      "description": "给用户看的中文执行说明"
    }}
  ]
}}
重要规则：

- 只输出 JSON，不要输出 Markdown。。
- 不允许输出 Python 代码。
- tool 必须来自可用工具列表，args 必须符合该 tool 的参数，不允许调用未列出的工具。
- 如果需要调用多个工具，需要按照调用顺序写在返回的actions列表中
- Houdini 场景上下文中的Selected Index属性代表当前节点在选中节点集合中的下标，为-1表示没有被选中
- 如果用户说“当前节点”，优先使用 Selected Index值为0的节点。
- 你需要分析我给你的当前 Houdini 场景上下文，特别是当前节点的连接关系，根据当前节点所连接的节点数量，选择合适的工具。
- 如果用户要求添加 smooth，new_node_type 使用 "smooth"。
- 如果用户要求添加 mountain，new_node_type 使用 "mountain"。
- description 必须是中文。
"""

    def build_user_prompt(self, text, context):
        prompt = """
用户请求：
{user_text}

当前 Houdini 场景上下文：
{context}
""".format(
            user_text=text,
            context=context
        )
        # print(context)
        return prompt
    def parse_json(self, content):
        try:
            return json.loads(content)
        except Exception:
            pass
        # 简单兼容模型输出 ```json ... ```
        try:
            content = content.strip()
            content = content.replace("```json", "")
            content = content.replace("```", "")
            return json.loads(content)
        except Exception as e:
            print("解析 LLM JSON 失败:")
            print(e)
            return None

    def build_plan(self, plan_data):
        actions_data = plan_data.get("actions", [])
        if not actions_data:
            return None
        plan = Plan()
        for item in actions_data:
            tool = item.get("tool")
            args = item.get("args", {})
            description = item.get("description", "")

            if not tool:
                continue

            plan.add_action(
                Action(
                    tool=tool,
                    args=args,
                    description=description
                )
            )

        if not plan.actions:
            return None

        return plan