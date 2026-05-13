# -*- coding: utf-8 -*-
from tools.base_tool import BaseTool
from houdini_adapter import parm_api

class GetParmTool(BaseTool):
    name = "get_parm"
    description = "获取指定路径的节点中的参数值"
    args_schema = {
        "node_path": "指定节点路径，比如/obj/geo1/box1",
        "parm_name": "需要获取的参数名，比如strength"
    }
    def run(self,
            node_path,
            parm_name):
        value = parm_api.get_parm_value(
            node_path,
            parm_name
        )
        return {
            "success": True,
            "value": value
        }