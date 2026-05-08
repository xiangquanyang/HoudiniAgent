# -*- coding: utf-8 -*-
from tools.base_tool import BaseTool
from houdini_adapter import node_api
class ConnectNodeTool(BaseTool):
    name = "connect_nodes"
    description = "Connect Houdini nodes"
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