# -*- coding: utf-8 -*-
from tools.base_tool import BaseTool
from houdini_adapter import graph_api

class GetDisplayNodeTool(BaseTool):
    """获取指定节点中激活display的节点"""
    name = "get_display_node"
    description = "Get display node"
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