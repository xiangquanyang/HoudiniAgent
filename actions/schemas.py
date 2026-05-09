# -*- coding: utf-8 -*-
class Action(object):
    """结构化存储需要调用的工具信息和参数信息"""
    def __init__(self, tool, args=None, description=""):
        self.tool = tool
        self.args = args or {}
        self.description = description
    def to_dict(self):
        return {
            "tool": self.tool,
            "args": self.args,
            "description": self.description
        }

    def to_preview_text(self):

        if self.description:
            return self.description

        return "{} {}".format(
            self.tool,
            self.args
        )