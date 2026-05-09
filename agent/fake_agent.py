# -*- coding: utf-8 -*-
from actions.plan import Plan
from actions.schemas import Action
from houdini_adapter import graph_api
from planner.graph_rewrite_planner import GraphRewritePlanner

class FakeAgent(object):
    def __init__(self):
        self.graph_rewrite_planner = GraphRewritePlanner()
    # --------------------------------
    # 生成Action
    # --------------------------------
    def run(self, text, context):
        text = text.lower()
        plan = Plan()
        # --------------------------------
        # 创建box + mountain
        # --------------------------------
        if "box" in text and "mountain" in text:
            # 1. 创建geo
            plan.add_action(
                Action(
                    tool="create_geo",
                    args={
                        "node_name": "geo_agent"
                    }
                )
            )
            # 2. 创建box
            plan.add_action(
                Action(
                    tool="create_node",
                    args={
                        "parent_path": "/obj/geo_agent",
                        "node_type": "box",
                        "node_name": "box1"
                    }
                )
            )
            # 3. 创建mountain
            plan.add_action(
                Action(
                    tool="create_node",
                    args={
                        "parent_path": "/obj/geo_agent",
                        "node_type": "mountain",
                        "node_name": "mountain1"
                    }
                )
            )
            # 4. 连接
            plan.add_action(
                Action(
                    tool="connect_nodes",
                    args={
                        "input_path": "/obj/geo_agent/box1",
                        "output_path": "/obj/geo_agent/mountain1"
                    }
                )
            )
            return plan

        if "smooth" in text and ("插入" in text or "添加" in text):

            selected_nodes = context.selected_nodes

            if not selected_nodes:
                return None

            current_node = selected_nodes[0]
            current_path = current_node["path"]

            return self.graph_rewrite_planner.plan_insert_after(
                source_node_path=current_path,
                new_node_type="smooth",
                new_node_name="smooth1",
                mode="auto"
            )

        return None

        # 在当前选中节点后面添加mountain节点
        if "mountain" in text:
            selected_nodes = context.selected_nodes
            if not selected_nodes:
                return None
            current_node = selected_nodes[0]
            current_path = current_node["path"]
            parent_path = current_path.rsplit("/", 1)[0]
            plan = Plan()
            # 创建mountain
            plan.add_action(
                Action(
                    tool="create_node",
                    args={
                        "parent_path": parent_path,
                        "node_type": "mountain",
                        "node_name": "mountain1"
                    }
                )
            )
            # 连接
            plan.add_action(
                Action(
                    tool="connect_nodes",
                    args={
                        "input_path": current_path,
                        "output_path":
                            parent_path + "/mountain1"
                    }
                )
            )
            return plan
        # 将mountain的noise变大
        if "height" in text and "大" in text:
            selected_nodes = context.selected_nodes
            if not selected_nodes:
                return None
            current_node = selected_nodes[0]
            node_path = current_node["path"]
            plan = Plan()
            # 先获取当前值
            plan.add_action(
                Action(
                    tool="get_parm",
                    args={
                        "node_path": node_path,
                        "parm_name": "height"
                    }
                )
            )
            # 再设置值
            plan.add_action(
                Action(
                    tool="set_parm",
                    args={
                        "node_path": node_path,
                        "parm_name": "height",
                        "value": 5
                    }
                )
            )
            return plan

        if "插入" in text and "smooth" in text:
            selected_nodes = context.selected_nodes
            if not selected_nodes:
                return None
            current_node = selected_nodes[0]
            current_path = current_node["path"]
            plan.add_action(
                Action(
                    tool="insert_shared_node",
                    args={
                        "source_node_path": current_path,
                        "new_node_type": "smooth",
                        "new_node_name": "smooth1"
                    }
                )
            )

            return plan

        if "smooth" in text:
            network_path = (
                context.current_network_path
            )
            plan = Plan()
            # 获取最后节点
            last_node_path = None
            # 这里暂时直接假设display node
            # 后面会动态执行结果传递
            display_node = graph_api.get_display_node(
                network_path
            )
            if display_node:
                last_node_path = display_node.path()
            if last_node_path is None:
                return None
            smooth_path = (
                    network_path + "/smooth1"
            )
            # 创建smooth
            plan.add_action(
                Action(
                    tool="create_node",
                    args={
                        "parent_path": network_path,
                        "node_type": "smooth",
                        "node_name": "smooth1"
                    }
                )
            )
            # 连接
            plan.add_action(
                Action(
                    tool="connect_nodes",
                    args={
                        "input_path": last_node_path,
                        "output_path": "$LAST_CREATED_NODE"
                    }
                )
            )
            return plan

        return None