# -*- coding: utf-8 -*-
class SceneContext(object):
    """保存当前network路径和选择的节点"""
    def __init__(self):
        self.selected_nodes = []
        self.current_network = None
        self.current_network_path = ""
    # --------------------------------
    # 转dict
    # --------------------------------
    def to_dict(self):
        return {
            "selected_nodes": self.selected_nodes,
            "current_network_path": self.current_network_path
        }