# -*- coding: utf-8 -*-
import hou
from houdini_adapter import topology_api
"""graph编辑相关代码"""
# --------------------------------
# 获取节点
# --------------------------------
def get_node(node_path):
    return hou.node(node_path)

# --------------------------------
# 插入节点
# --------------------------------
def insert_node_between(
        input_node_path,
        output_node_path,
        new_node_type,
        new_node_name=None):
    input_node = get_node(
        input_node_path
    )
    output_node = get_node(
        output_node_path
    )
    if input_node is None:
        return None
    if output_node is None:
        return None
    parent = output_node.parent()

    # --------------------------------
    # 获取原始slot，获取input_node_path节点是output_node_path节点的第几号输入
    # --------------------------------
    slot_index = (
        topology_api.get_input_slot(
            output_node_path,
            input_node_path
        )
    )

    # 创建新节点
    new_node = parent.createNode(
        new_node_type,
        node_name=new_node_name
    )
    # --------------------------------
    # 重新连接
    # --------------------------------
    # input -> new
    new_node.setInput(0, input_node)
    # new -> output
    output_node.setInput(slot_index, new_node)
    new_node.moveToGoodPosition()
    parent.layoutChildren()
    return new_node