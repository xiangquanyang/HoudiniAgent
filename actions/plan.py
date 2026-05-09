# -*- coding: utf-8 -*-
class Plan(object):
    """存放Action对象的列表"""
    def __init__(self, actions=None):
        self.actions = actions or []
    # --------------------------------
    # 添加Action
    # --------------------------------
    def add_action(self, action):
        self.actions.append(action)
    # --------------------------------
    # 转dict
    # --------------------------------
    def to_dict(self):
        return [
            action.to_dict()
            for action in self.actions
        ]


    def to_preview_text(self):
        """输出Plan信息"""
        lines = []
        for index, action in enumerate(self.actions):
            lines.append(
                "{}. {}".format(
                    index + 1,
                    action.to_preview_text()
                )
            )
        return "\n".join(lines)