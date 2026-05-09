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
    def get_downstream_nodes(self, node_path):
        edges = self.get_edges(node_path)

        result = []
        for edge in edges:
            result.append(edge.output_node_path)

        return result

    # 获取node_path节点输出连接节点数量
    def get_output_count(self, node_path):
        return len(self.get_edges(node_path))

    # 判断node_path节点是否有连接输出
    def has_outputs(self, node_path):
        return self.get_output_count(node_path) > 0

    # 判断node_path节点是否有连接多个输出
    def is_branch_node(self, node_path):
        return self.get_output_count(node_path) > 1