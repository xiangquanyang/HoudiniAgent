# -*- coding: utf-8 -*-
import os
import pkgutil
import importlib
import inspect

from tools.base_tool import BaseTool

class ToolRegistry(object):
    def __init__(self):
        self.tools = {}
        self.auto_discover_tools()
    # --------------------------------
    # 自动发现 tools 包下所有 *_tool.py
    # --------------------------------
    def auto_discover_tools(self):
        import tools
        package_path = os.path.dirname(
            tools.__file__
        )
        package_name = tools.__name__
        for finder, module_name, is_pkg in pkgutil.walk_packages(
                [package_path],
                prefix=package_name + "."):
            if is_pkg:
                continue
            # 只加载 xxx_tool.py
            if not module_name.endswith("_tool"):
                continue
            module = importlib.import_module(
                module_name
            )
            self.register_tools_from_module(
                module
            )
    # --------------------------------
    # 从模块中查找 BaseTool 子类
    # --------------------------------
    def register_tools_from_module(self, module):
        for name, obj in inspect.getmembers(
                module,
                inspect.isclass):
            if obj is BaseTool:
                continue
            if not issubclass(obj, BaseTool):
                continue
            # 避免导入别的模块里 import 进来的 Tool 类被重复注册
            if obj.__module__ != module.__name__:
                continue
            tool = obj()
            self.register(tool)

    # --------------------------------
    # 注册单个 Tool
    # --------------------------------
    def register(self, tool):
        if not tool.name:
            raise ValueError(
                "Tool name is empty: {}".format(
                    tool.__class__.__name__
                )
            )

        if tool.name in self.tools:
            raise ValueError(
                "Duplicate tool name: {}".format(
                    tool.name
                )
            )

        self.tools[tool.name] = tool
        print(
            "[ToolRegistry] registered tool:",
            tool.name
        )

    # --------------------------------
    # 获取 Tool
    # --------------------------------
    def get_tool(self, tool_name):
        return self.tools.get(tool_name)

    # --------------------------------
    # 获取所有 Tool
    # --------------------------------
    def get_all_tools(self):
        return list(self.tools.values())

    # --------------------------------
    # 生成 Prompt Tool 信息
    # --------------------------------
    def get_prompt_text(self):
        print("==================get_all_tools=================")
        tools = []
        tools_info = []
        for tool in self.get_all_tools():
            tools_info.append(tool.__class__.get_prompt_info())
        print('-----------get_prompt_info-----------')
        res = "\n".join(tools_info)
        print(res)
        return res