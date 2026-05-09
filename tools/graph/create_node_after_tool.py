# -*- coding: utf-8 -*-
from tools.base_tool import BaseTool
from houdini_adapter import node_api


class CreateNodeAfterTool(BaseTool):
    name = "create_node_after"
    description = "Create node after source node"
    def run(self,
            source_node_path,
            new_node_type,
            new_node_name=None):
        source_node = node_api.get_node(source_node_path)
        if source_node is None:
            return {
                "success": False,
                "message": "Source node not found"
            }
        parent = source_node.parent()
        new_node = node_api.create_sop_node(
            parent=parent,
            node_type=new_node_type,
            node_name=new_node_name
        )
        new_node.setInput(0, source_node)
        parent.layoutChildren()
        return {
            "success": True,
            "node_path": new_node.path()
        }