# -*- coding: utf-8 -*-
from tools.base_tool import BaseTool
from houdini_adapter import parm_api

class InspectParmTool(BaseTool):
    """获取节点所有可以设置的参数信息"""
    name = "inspect_parms"
    description = "获取指定节点上所有可以设置的参数信息"
    args_schema = {
        "node_path": "指定节点路径，比如/obj/geo1/box1"
    }
    def run(self,
            node_path):
        parms = parm_api.get_parm_info(
            node_path
        )
        return {
            "success": True,
            "parms": parms
        }