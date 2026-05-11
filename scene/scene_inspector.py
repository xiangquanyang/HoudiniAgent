# -*- coding: utf-8 -*-

from scene.scene_context import SceneContext
from houdini_adapter import scene_api
from houdini_adapter.graph_api import get_network_connection

class SceneInspector(object):
    # --------------------------------
    # 构建Scene Context
    # --------------------------------
    def build_context(self):
        context = SceneContext()
        # --------------------------------
        # 获取当前选择的所有节点
        # --------------------------------
        selected_nodes = scene_api.get_selected_nodes()
        # 往context中存放选中的节点的信息
        for node in selected_nodes:
            context.selected_nodes.append({
                "name": node.name(),
                "path": node.path(),
                "type": node.type().name()
            })
        # --------------------------------
        # 获取当前所在network路径
        # --------------------------------
        network = scene_api.get_current_network()
        # 往context中存放当前network信息
        if network:
            context.current_network = network
            context.current_network_path = (
                network.path()
            )
        return context

    def get_network_connection(self):
        return get_network_connection()