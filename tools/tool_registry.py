# -*- coding: utf-8 -*-
from tools.create_geo_tool import CreateGeoTool
from tools.create_node_tool import CreateNodeTool
from tools.connect_node_tool import ConnectNodeTool
from tools.set_parm_tool import SetParmTool
from tools.get_parm_tool import GetParmTool
from tools.inspect_parm_tool import (
    InspectParmTool
)
from tools.graph.get_display_node_tool import (
    GetDisplayNodeTool
)
from tools.graph.get_last_node_tool import (
    GetLastNodeTool
)
from tools.graph.insert_node_tool import (
    InsertNodeTool
)
from tools.graph.insert_shared_node_tool import InsertSharedNodeTool

class ToolRegistry(object):
    """
    对工具类对象登记
    """
    def __init__(self):
        self.tools = {}
        self.register(CreateGeoTool())
        self.register(CreateNodeTool())
        self.register(ConnectNodeTool())
        self.register(SetParmTool())
        self.register(GetParmTool())
        self.register(InspectParmTool())
        self.register(GetDisplayNodeTool())
        self.register(GetLastNodeTool())
        self.register(InsertNodeTool())
        self.register(InsertSharedNodeTool())
    # -----------------------------
    # 注册Tool
    # -----------------------------
    def register(self, tool):
        self.tools[tool.name] = tool
    # -----------------------------
    # 获取Tool
    # -----------------------------
    def get_tool(self, tool_name):
        return self.tools.get(tool_name)