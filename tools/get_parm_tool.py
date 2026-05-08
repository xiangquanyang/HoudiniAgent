# -*- coding: utf-8 -*-
from tools.base_tool import BaseTool
from houdini_adapter import parm_api

class GetParmTool(BaseTool):
    name = "get_parm"
    description = "Get Houdini parameter"
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