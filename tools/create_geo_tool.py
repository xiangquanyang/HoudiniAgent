# -*- coding: utf-8 -*-
from tools.base_tool import BaseTool
from houdini_adapter import node_api
class CreateGeoTool(BaseTool):
    name = "create_geo"
    description = "Create Geometry Container"
    def run(self, node_name="geo1"):
        geo = node_api.create_geo_container(
            name=node_name
        )
        node_api.clear_geo_children(geo)
        return {
            "success": True,
            "node_path": geo.path()
        }