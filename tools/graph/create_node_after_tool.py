# -*- coding: utf-8 -*-
from tools.base_tool import BaseTool
from houdini_adapter import node_api


class CreateNodeAfterTool(BaseTool):
    name = "create_node_after"
    description = "在指定 Houdini 节点后创建并连接一个新的 SOP 节点，如果源节点后面没有连接任何节点，使用当前工具。"
    args_schema = {
        "source_node_path": "源节点路径，例如 /obj/geo1/box1",
        "new_node_type": "要创建的 SOP 节点类型，例如 smooth、mountain、null",
        "new_node_name": "新节点名称，不能为空，不能和已有节点名字相同"
    }
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