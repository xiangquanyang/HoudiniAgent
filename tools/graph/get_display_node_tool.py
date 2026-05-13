# -*- coding: utf-8 -*-
from tools.base_tool import BaseTool
from houdini_adapter import graph_api

class GetDisplayNodeTool(BaseTool):
    """获取指定节点中激活display的节点"""
    name = "get_display_node"
    description = "获取指定路径的network中所激活display flag的节点"
    args_schema = {
        "network_path": "指定节点的路径，例如 /obj/geo1/"
    }
    def run(self, network_path):
        node = graph_api.get_display_node(
            network_path
        )
        if node is None:
            return {
                "success": False
            }
        return {
            "success": True,
            "node_path": node.path(),
            "node_name": node.name()
        }