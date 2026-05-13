# -*- coding: utf-8 -*-

import os
import json


class AgentMemory(object):

    def __init__(self, memory_path=None):
        if memory_path is None:
            current_dir = os.path.dirname(__file__)
            memory_path = os.path.join(
                current_dir,
                "agent_memory.json"
            )

        self.memory_path = memory_path

        self.created_nodes = []
        self.executed_actions = []

        self.load()

    # --------------------------------
    # 记录 Action
    # --------------------------------
    def remember_action(self, action, result):

        self.executed_actions.append({
            "tool": action.tool,
            "args": action.args,
            "result": result
        })

        node_path = result.get("node_path")

        if node_path:

            self.created_nodes.append({
                "node_path": node_path,
                "node_type": self.guess_node_type(action),
                "source_tool": action.tool
            })

        self.save()

    # --------------------------------
    # 推断节点类型
    # --------------------------------
    def guess_node_type(self, action):

        args = action.args

        if "new_node_type" in args:
            return args["new_node_type"]

        if "node_type" in args:
            return args["node_type"]

        return ""

    # --------------------------------
    # 查询创建过的节点
    # --------------------------------
    def find_created_nodes_by_type(self, node_type):

        result = []

        for item in self.created_nodes:
            if item.get("node_type") == node_type:
                result.append(item)

        return result

    # --------------------------------
    # 给 LLM 用的文本
    # --------------------------------
    def to_prompt_text(self):

        lines = []
        lines.append("Agent 之前创建过的节点：")

        if not self.created_nodes:
            lines.append("- 无")
        else:
            for item in self.created_nodes:
                lines.append(
                    "- path: {path}, type: {type}, source_tool: {tool}".format(
                        path=item.get("node_path"),
                        type=item.get("node_type"),
                        tool=item.get("source_tool")
                    )
                )

        return "\n".join(lines)

    # --------------------------------
    # 转 dict
    # --------------------------------
    def to_dict(self):

        return {
            "created_nodes": self.created_nodes,
            "executed_actions": self.executed_actions
        }

    # --------------------------------
    # 从 dict 恢复
    # --------------------------------
    def from_dict(self, data):

        self.created_nodes = data.get(
            "created_nodes",
            []
        )

        self.executed_actions = data.get(
            "executed_actions",
            []
        )

    # --------------------------------
    # 保存 JSON
    # --------------------------------
    def save(self):

        folder = os.path.dirname(
            self.memory_path
        )

        if not os.path.exists(folder):
            os.makedirs(folder)

        data = self.to_dict()

        with open(self.memory_path, "w") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

    # --------------------------------
    # 加载 JSON
    # --------------------------------
    def load(self):

        if not os.path.exists(self.memory_path):
            return

        try:
            with open(self.memory_path, "r") as f:
                data = json.load(f)

            self.from_dict(data)

        except Exception as e:
            print("[AgentMemory] load failed:")
            print(e)

    # --------------------------------
    # 清空记忆
    # --------------------------------
    def clear(self):

        self.created_nodes = []
        self.executed_actions = []

        self.save()