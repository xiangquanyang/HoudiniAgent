# -*- coding: utf-8 -*-
from tools.base_tool import BaseTool
from houdini_adapter import graph_api

class GetLastNodeTool(BaseTool):
    name = "get_last_node"
    description = "获取指定路径的network下的最后一个节点"
    args_schema = {
        "network_path": "指定节点的路径，例如 /obj/geo1/"
    }
    def run(self, network_path):
        node = graph_api.get_last_node(
            network_path
        )
        if node is None:
            return {
                "success": False
            }
        return {
            "success": True,
            "node_path": node.path()
        }