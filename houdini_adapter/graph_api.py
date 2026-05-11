# -*- coding: utf-8 -*-
import hou
import traceback
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





def s(v):
    try:
        return str(v)
    except Exception:
        try:
            return repr(v)
        except Exception:
            return "<unprintable>"


def w(lines, text=""):
    lines.append(text)


def header(lines, title):
    w(lines, "")
    w(lines, "=" * 120)
    w(lines, title)
    w(lines, "=" * 120)


def safe_eval_parm(parm):
    try:
        return parm.eval()
    except Exception:
        try:
            return parm.rawValue()
        except Exception:
            return "<unreadable>"


def dump_node_basic(lines, node, selected_index):
    header(lines, "NODE BASIC INFO")

    w(lines, "Path              : %s" % node.path())
    w(lines, "Name              : %s" % node.name())
    w(lines, "Selected Index    : %s" % selected_index)
    w(lines, "Type              : %s" % s(node.type().name()))
    w(lines, "Category          : %s" % s(node.type().category().name()))
    w(lines, "Description       : %s" % s(node.type().description()))
    w(lines, "Parent            : %s" % s(node.parent().path() if node.parent() else None))


def dump_node_connections(lines, node):
    header(lines, "NODE CONNECTIONS")
    w(lines, "[Inputs]")
    input_conns = node.inputConnections()
    if not input_conns:
        w(lines, "  <none>")
    else:
        for conn in input_conns:
            try:
                src_node = conn.inputNode()
            except Exception:
                src_node = None
            try:
                dst_node = conn.outputNode()
            except Exception:
                dst_node = node
            w(lines, "  %s -> %s" % (
                src_node.path() if src_node else "<none>",
                dst_node.path() if dst_node else "<none>"
            ))


def dump_parms(lines, node):
    header(lines, "PARAMETERS")
    parm_tuples = node.parmTuples()
    if not parm_tuples:
        w(lines, "<no parms>")
        return
    for pt in parm_tuples:
        w(lines, "-" * 120)
        try:
            pt_name = pt.name()
        except Exception:
            pt_name = "<unknown>"
        w(lines, "ParmTuple: %s" % pt_name)
        for parm in pt:
            try:
                parm_name = parm.name()
            except Exception:
                parm_name = "<unknown>"
            value = safe_eval_parm(parm)
            w(lines, "  Parm  : %s" % parm_name)
            w(lines, "  Value : %s" % s(value))
            w(lines, "")


def get_network_connection():
    """获取当前Network中显示的所有节点的连接信息"""
    pane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    current_network = pane.pwd()
    nodes = current_network.children()
    selected_nodes = hou.selectedNodes()
    if not nodes:
        raise RuntimeError("No Houdini nodes.")
    lines = []
    header(lines, "HOUDINI CURRENT NETWORK")
    w(lines, "Network Path : %s" % current_network.path())
    w(lines, "Node Count   : %s" % len(nodes))
    for i, node in enumerate(nodes, 1):
        selected_index = -1
        for j, selected_node in enumerate(selected_nodes):
            if node == selected_node:
                selected_index = j
        header(lines, "NODE %s" % i)
        dump_node_basic(lines, node, selected_index)
        dump_node_connections(lines, node)
        dump_parms(lines, node)
    return "\n".join(lines)