# -*- coding: utf-8 -*-
import hou
from houdini_adapter import topology_api
"""graph编辑相关代码"""
# --------------------------------
# 获取节点
# --------------------------------
def get_node(node_path):
    return hou.node(node_path)
# 目标：
# box1
#  ├── mountain1
#  └── null1
# 调用下面的插入方法后变成：
# box1
#  ↓
# smooth1
#  ├── mountain1
#  └── null1
def insert_shared_node_after(
        source_node_path,
        new_node_type,
        new_node_name=None):
    source_node = get_node(source_node_path)
    if source_node is None:
        return None
    parent = source_node.parent()
    output_nodes = source_node.outputs()
    if not output_nodes:
        return None
    # 记录原始输出关系
    connections = []
    for output_node in output_nodes:
        slot_index = topology_api.get_input_slot(
            output_node.path(),
            source_node.path()
        )
        if slot_index is None:
            continue
        connections.append({
            "output_node": output_node,
            "slot_index": slot_index
        })
    if not connections:
        return None
    # 创建共享新节点
    print("--------------new_node_type-----------")
    print(new_node_type)
    print("--------------new_node_name-----------")
    print(new_node_name)
    new_node = parent.createNode(
        new_node_type,
        node_name=new_node_name
    )

    # source -> new_node
    new_node.setInput(0, source_node)

    # new_node -> 所有原始下游
    for conn in connections:

        conn["output_node"].setInput(
            conn["slot_index"],
            new_node
        )

    new_node.moveToGoodPosition()
    parent.layoutChildren()

    return new_node


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