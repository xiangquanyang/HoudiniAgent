# -*- coding: utf-8 -*-

from tools.base_tool import BaseTool
from houdini_adapter import node_api


class CreateNodeTool(BaseTool):
    # 会将name作为key注册到tool_registry中
    name = "create_node"
    description = "在指定路径的Network下创建一个新的节点"
    args_schema = {
        "parent_path": "指定创建节点所在的Network路径，比如/obj/geo1",
        "node_type": "创建的节点类型名，比如box",
        "node_name": "创建的节点名，不能为空，不能和所在的Network下已有节点重名",
    }
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