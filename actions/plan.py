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