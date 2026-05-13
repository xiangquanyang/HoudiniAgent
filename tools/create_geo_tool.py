# -*- coding: utf-8 -*-
from tools.base_tool import BaseTool
from houdini_adapter import node_api
class CreateGeoTool(BaseTool):
    name = "create_geo"
    description = "在/obj下创建一个geo节点"
    args_schema = {
        "node_name": "geo节点名，不能为空，不能和/obj下其他节点重名"
    }
    def run(self, node_name="geo1"):
        geo = node_api.create_geo_container(
            name=node_name
        )
        node_api.clear_geo_children(geo)
        return {
            "success": True,
            "node_path": geo.path()
        }