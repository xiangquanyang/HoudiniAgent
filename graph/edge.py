# -*- coding: utf-8 -*-
class Edge(object):
    def __init__(self,
                 input_node_path,
                 output_node_path,
                 slot_index):
        self.input_node_path = (
            input_node_path
        )
        self.output_node_path = (
            output_node_path
        )
        self.slot_index = slot_index
    # --------------------------------
    # 转dict
    # --------------------------------
    def to_dict(self):
        return {
            "input_node":
                self.input_node_path,
            "output_node":
                self.output_node_path,
            "slot":
                self.slot_index
        }