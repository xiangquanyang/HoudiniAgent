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
    description = "在一个 Houdini 节点后插入一个共享 SOP 节点，并保持所有下游连接。如果源节点连接了多个下游节点，在插入节点时使用当前工具。"

    args_schema = {
        "source_node_path": "源节点路径",
        "new_node_type": "要插入的 SOP 节点类型",
        "new_node_name": "新节点名称，不能为空，不能和已有节点名字相同"
    }
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