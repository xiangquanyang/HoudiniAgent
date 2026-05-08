# -*- coding: utf-8 -*-

from tools.base_tool import BaseTool
from houdini_adapter import (
    graph_edit_api
)

class InsertNodeTool(BaseTool):
    name = "insert_node"
    description = "Insert node between nodes"
    def run(self,
            input_node_path,
            output_node_path,
            new_node_type,
            new_node_name=None):
        node = (
            graph_edit_api.insert_node_between(
                input_node_path=input_node_path,
                output_node_path=output_node_path,
                new_node_type=new_node_type,
                new_node_name=new_node_name
            )
        )
        if node is None:
            return {
                "success": False
            }
        return {
            "success": True,
            "node_path": node.path()
        }