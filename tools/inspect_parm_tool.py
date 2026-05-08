# -*- coding: utf-8 -*-
from tools.base_tool import BaseTool
from houdini_adapter import parm_api

class InspectParmTool(BaseTool):
    """获取节点所有可以设置的参数信息"""
    name = "inspect_parms"
    description = "Inspect node parms"
    def run(self,
            node_path):
        parms = parm_api.get_parm_info(
            node_path
        )
        return {
            "success": True,
            "parms": parms
        }