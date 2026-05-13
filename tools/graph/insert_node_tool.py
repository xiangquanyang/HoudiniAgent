# -*- coding: utf-8 -*-

from tools.base_tool import BaseTool
from houdini_adapter import (
    graph_edit_api
)

class InsertNodeTool(BaseTool):
    name = "insert_node"
    description = "在指定 Houdini 节点后创建并连接一个新的 SOP 节点，如果源节点后面连接了单个节点，使用当前工具。"
    args_schema = {
        "input_node_path": "源节点路径",
        "output_node_path": "源节点所连接的下游节点路径",
        "new_node_type": "要插入的 SOP 节点类型",
        "new_node_name": "新节点名称，不能为空，不能和已有节点名字相同"
    }
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