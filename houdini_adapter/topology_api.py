# -*- coding: utf-8 -*-
import hou

# --------------------------------
# 获取节点
# --------------------------------
def get_node(node_path):
    return hou.node(node_path)

# --------------------------------
# 获取输入slot
# 判断input_node_path节点是output_node_path节点的几号输入
# --------------------------------
def get_input_slot(output_node_path,
                   input_node_path):
    output_node = get_node(
        output_node_path
    )
    input_node = get_node(
        input_node_path
    )
    if output_node is None:
        return None
    if input_node is None:
        return None
    inputs = output_node.inputs()
    for index, node in enumerate(inputs):
        if node == input_node:
            return index
    return None