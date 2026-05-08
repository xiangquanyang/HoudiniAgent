# -*- coding: utf-8 -*-

from tools.base_tool import BaseTool
from houdini_adapter import node_api


class CreateNodeTool(BaseTool):
    # 会将name作为key注册到tool_registry中
    name = "create_node"
    description = "Create Houdini node"
    def run(self,
            parent_path,
            node_type,
            node_name=None):
        print("=" * 50)
        print("CreateNodeTool")
        parent = node_api.get_node(parent_path)
        node = node_api.create_sop_node(
            parent=parent,
            node_type=node_type,
            node_name=node_name
        )

        return {
            "success": True,
            "node_path": node.path()
        }