# -*- coding: utf-8 -*-
class Action(object):
    """结构化存储需要调用的工具信息和参数信息"""
    def __init__(self,
                 tool,
                 args=None):
        self.tool = tool
        self.args = args or {}
    def to_dict(self):
        return {
            "tool": self.tool,
            "args": self.args
        }