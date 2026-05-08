# -*- coding: utf-8 -*-
import hou
"""与操作节点参数相关代码"""

# --------------------------------
# 获取节点
# --------------------------------
def get_node(node_path):
    return hou.node(node_path)

# --------------------------------
# 获取参数
# --------------------------------
def get_parm(node_path,
             parm_name):
    node = get_node(node_path)
    if node is None:
        return None
    return node.parm(parm_name)

# --------------------------------
# 获取参数值
# --------------------------------
def get_parm_value(node_path,
                   parm_name):
    parm = get_parm(
        node_path,
        parm_name
    )
    if parm is None:
        return None
    return parm.eval()

# --------------------------------
# 设置参数值
# --------------------------------
def set_parm_value(node_path,
                   parm_name,
                   value):
    parm = get_parm(
        node_path,
        parm_name
    )
    if parm is None:
        return False
    parm.set(value)
    return True


# --------------------------------
# 获取所有参数
# --------------------------------
def get_all_parms(node_path):
    node = get_node(node_path)
    if node is None:
        return []
    return node.parms()


# --------------------------------
# 获取节点所有参数信息
# --------------------------------
def get_parm_info(node_path):
    node = get_node(node_path)
    if node is None:
        return []
    parm_infos = []
    for parm in node.parms():
        parm_infos.append({
            "name": parm.name(),
            "label": parm.description(),
            "value": parm.eval()
        })
    return parm_infos