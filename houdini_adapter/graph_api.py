# -*- coding: utf-8 -*-
import hou
from graph.edge import Edge
"""获取节点连接关系相关代码"""
# --------------------------------
# 获取节点
# --------------------------------
def get_node(node_path):
    return hou.node(node_path)

# --------------------------------
# 获取所有输出连接
# 获取node_path节点所连接的所有节点信息，包括是下游节点的几号输入
# --------------------------------
def get_output_edges(node_path):
    node = get_node(node_path)
    if node is None:
        return []
    edges = []
    for output_node in node.outputs():
        # 找到slot
        inputs = output_node.inputs()
        for slot_index, input_node in enumerate(inputs):
            if input_node == node:
                edge = Edge(
                    input_node_path=node.path(),
                    output_node_path=output_node.path(),
                    slot_index=slot_index
                )
                edges.append(edge)
    return edges


# --------------------------------
# 获取输入节点
# --------------------------------
def get_input_nodes(node_path):
    node = get_node(node_path)
    if node is None:
        return []
    inputs = []
    for input_node in node.inputs():
        if input_node:
            inputs.append(input_node)
    return inputs

# --------------------------------
# 获取输出节点
# --------------------------------
def get_output_nodes(node_path):
    node = get_node(node_path)
    if node is None:
        return []
    outputs = []
    for output_node in node.outputs():
        outputs.append(output_node)
    return outputs

# --------------------------------
# 获取display节点
# --------------------------------
def get_display_node(network_path):
    network = get_node(network_path)
    if network is None:
        return None
    for child in network.children():
        if child.isDisplayFlagSet():
            return child
    return None

# --------------------------------
# 获取network_path路径最后节点
# --------------------------------
def get_last_node(network_path):
    display_node = get_display_node(
        network_path
    )
    if display_node:
        return display_node
    network = get_node(network_path)
    if network is None:
        return None
    children = network.children()
    if not children:
        return None
    return children[-1]

# --------------------------------
# 获取node_path节点的第一个输出节点
# --------------------------------
def get_first_output_node(node_path):
    node = get_node(node_path)
    if node is None:
        return None
    outputs = node.outputs()
    if not outputs:
        return None
    return outputs[0]