# -*- coding: utf-8 -*-
class BaseTool(object):
    name = "base_tool"
    description = ""
    def run(self, *args, **kwargs):
        raise NotImplementedError