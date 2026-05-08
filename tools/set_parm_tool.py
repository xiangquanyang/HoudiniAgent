# -*- coding: utf-8 -*-
from tools.base_tool import BaseTool
from houdini_adapter import parm_api

class SetParmTool(BaseTool):
    name = "set_parm"
    description = "Set Houdini parameter"
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