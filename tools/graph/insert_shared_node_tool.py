# -*- coding: utf-8 -*-
from tools.base_tool import BaseTool
from houdini_adapter import graph_edit_api

# 目标：
# box1
#  ├── mountain1
#  └── null1
# 调用run方法后变成：
# box1
#  ↓
# smooth1
#  ├── mountain1
#  └── null1
class InsertSharedNodeTool(BaseTool):
    name = "insert_shared_node"
    description = "Insert one shared node after source node and reconnect all downstream nodes"
    def run(self,
            source_node_path,
            new_node_type,
            new_node_name=None):
        node = graph_edit_api.insert_shared_node_after(
            source_node_path=source_node_path,
            new_node_type=new_node_type,
            new_node_name=new_node_name
        )
        if node is None:
            return {
                "success": False,
                "message": "Insert shared node failed"
            }
        return {
            "success": True,
            "node_path": node.path()
        }