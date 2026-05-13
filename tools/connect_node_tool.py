# -*- coding: utf-8 -*-
from tools.base_tool import BaseTool
from houdini_adapter import node_api
class ConnectNodeTool(BaseTool):
    name = "connect_node"
    description = "将上游节点连接到下游节点0号输入端口"
    args_schema = {
        "input_path": "上游节点路径",
        "output_path": "下游节点路径"
    }
    def run(self,
            input_path,
            output_path):
        input_node = node_api.get_node(input_path)
        output_node = node_api.get_node(output_path)
        node_api.connect_nodes(
            input_node,
            output_node
        )
        return {
            "success": True
        }