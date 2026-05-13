# -*- coding: utf-8 -*-
class BaseTool(object):
    name = ""
    description = ""
    args_schema = {}
    def run(self, **kwargs):
        raise NotImplementedError

    @classmethod
    def get_prompt_info(cls):
        arg_lines = []
        for arg_name, arg_desc in cls.args_schema.items():
            arg_lines.append(
                "- {}: {}".format(arg_name, arg_desc)
            )
        return """
工具名：{name}
用途：{description}
参数：
{args}
""".format(
            name=cls.name,
            description=cls.description,
            args="\n".join(arg_lines)
        )