# -*- coding: utf-8 -*-
from tools.base_tool import BaseTool
from houdini_adapter import parm_api

class SetParmTool(BaseTool):
    name = "set_parm"
    description = "设置指定 Houdini 节点的参数值。"
    args_schema = {
        "node_path": "节点路径",
        "parm_name": "参数名称，例如 height、scale、tx",
        "value": "参数值"
    }
    def run(self,
            node_path,
            parm_name,
            value):
        success = parm_api.set_parm_value(
            node_path,
            parm_name,
            value
        )
        return {
            "success": success
        }