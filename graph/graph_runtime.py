# -*- coding: utf-8 -*-
from houdini_adapter import graph_api

class GraphRuntime(object):
    # --------------------------------
    # 获取节点所有边
    # --------------------------------
    def get_edges(self,
                  node_path):
        return graph_api.get_output_edges(
            node_path
        )
    # --------------------------------
    # 获取下游节点
    # --------------------------------
    def get_downstream_nodes(
            self,
            node_path):
        edges = self.get_edges(
            node_path
        )
        result = []
        for edge in edges:
            result.append(
                edge.output_node_path
            )
        return result