# -*- coding: utf-8 -*-
class VariableResolver(object):
    """解析动态变量"""
    # --------------------------------
    # 解析变量
    # --------------------------------
    @classmethod
    def resolve_args(cls,
                     args,
                     execution_context):
        resolved = {}
        for key, value in args.items():
            resolved[key] = cls.resolve_value(
                value,
                execution_context
            )
        return resolved

    # --------------------------------
    # 解析单个值
    # --------------------------------
    @classmethod
    def resolve_value(cls,
                      value,
                      execution_context):
        if value == "$LAST_CREATED_NODE":
            return (
                execution_context
                .last_created_node
            )

        return value