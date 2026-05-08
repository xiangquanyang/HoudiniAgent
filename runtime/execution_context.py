# -*- coding: utf-8 -*-
class ExecutionContext(object):
    """保存当前Action执行后的状态"""
    def __init__(self):
        # 最后创建节点
        self.last_created_node = None
        # 当前节点
        self.current_node = None
        # Action结果
        self.action_results = []

    # --------------------------------
    # 设置最后创建节点
    # --------------------------------
    def set_last_created_node(
            self,
            node_path):
        self.last_created_node = node_path

    # --------------------------------
    # 添加Action结果
    # --------------------------------
    def add_result(self, result):
        self.action_results.append(result)

    # --------------------------------
    # 转dict
    # --------------------------------
    def to_dict(self):
        return {
            "last_created_node":
                self.last_created_node,
            "current_node":
                self.current_node,
            "action_results":
                self.action_results
        }