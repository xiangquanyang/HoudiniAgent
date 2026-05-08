# -*- coding: utf-8 -*-
"""
与操作场景相关代码
"""
import hou


# --------------------------------
# 获取当前选择节点
# --------------------------------
def get_selected_nodes():
    return hou.selectedNodes()


# --------------------------------
# 获取当前Network Editor路径
# --------------------------------
def get_current_network():
    pane = hou.ui.paneTabOfType(
        hou.paneTabType.NetworkEditor
    )
    if pane is None:
        return None
    return pane.pwd()

# --------------------------------
# 获取子节点
# --------------------------------
def get_children(node):
    return node.children()


# --------------------------------
# 获取节点类型
# --------------------------------
def get_node_type(node):
    return node.type().name()


# --------------------------------
# 获取节点路径
# --------------------------------
def get_node_path(node):
    return node.path()