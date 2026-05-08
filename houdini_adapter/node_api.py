# -*- coding: utf-8 -*-
import hou
"""
与操作节点相关的代码
"""

def get_node(path):
    return hou.node(path)
# --------------------------------
# 创建Geometry Container
# --------------------------------
def create_geo_container(name="geo1"):
    obj = hou.node("/obj")
    geo = obj.createNode(
        "geo",
        node_name=name
    )
    geo.moveToGoodPosition()
    return geo
# --------------------------------
# 删除默认file节点
# --------------------------------
def clear_geo_children(geo_node):
    for child in geo_node.children():
        child.destroy()
# --------------------------------
# 创建SOP节点
# --------------------------------
def create_sop_node(parent,
                    node_type,
                    node_name=None):
    node = parent.createNode(
        node_type,
        node_name=node_name
    )
    node.moveToGoodPosition()
    return node
# --------------------------------
# 连接节点
# --------------------------------
def connect_nodes(input_node,
                  output_node):
    output_node.setInput(0, input_node)
# --------------------------------
# 自动布局
# --------------------------------
def layout_children(parent):
    parent.layoutChildren()