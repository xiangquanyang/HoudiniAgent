# -*- coding: utf-8 -*-
from actions.schemas import Action
from actions.plan import Plan
from graph.graph_runtime import GraphRuntime

class GraphRewritePlanner(object):

    def __init__(self):
        self.graph_runtime = GraphRuntime()

    # --------------------------------
    # 在节点后插入节点
    # 根据source_node_path节点状态，自动选择插入方式，返回Plan
    # --------------------------------
    def plan_insert_after(
            self,
            source_node_path,
            new_node_type,
            new_node_name=None,
            mode="auto"):
        """
        mode:
            auto        自动判断
            shared      多输出时共享一个新节点
            per_edge    多输出时每条边插一个新节点
            append      没有输出时直接追加
        """

        plan = Plan()

        output_count = self.graph_runtime.get_output_count(
            source_node_path
        )

        # 没有下游节点：直接创建并连接
        if output_count == 0:
            plan.add_action(
                Action(
                    tool="create_node_after",
                    args={
                        "source_node_path": source_node_path,
                        "new_node_type": new_node_type,
                        "new_node_name": new_node_name
                    },
                    description="在 {} 后创建并连接一个 {} 节点".format(
                        source_node_path,
                        new_node_type
                    )
                )
            )
            return plan

        # 单输出：普通插入
        if output_count == 1:
            edges = self.graph_runtime.get_edges(source_node_path)
            edge = edges[0]

            plan.add_action(
                Action(
                    tool="insert_node",
                    args={
                        "input_node_path": edge.input_node_path,
                        "output_node_path": edge.output_node_path,
                        "new_node_type": new_node_type,
                        "new_node_name": new_node_name
                    },
                    description="在 {} 和 {} 之间插入 {} 节点".format(
                        edge.input_node_path,
                        edge.output_node_path,
                        new_node_type
                    )
                )
            )
            return plan

        # 多输出：根据策略决定
        if mode == "per_edge":
            edges = self.graph_runtime.get_edges(source_node_path)

            for index, edge in enumerate(edges):
                node_name = None
                if new_node_name:
                    node_name = "{}_{}".format(
                        new_node_name,
                        index + 1
                    )

                plan.add_action(
                    Action(
                        tool="insert_node",
                        args={
                            "input_node_path": edge.input_node_path,
                            "output_node_path": edge.output_node_path,
                            "new_node_type": new_node_type,
                            "new_node_name": node_name
                        }
                    )
                )

            return plan

        # 默认：多输出共享一个节点
        plan.add_action(
            Action(
                tool="insert_shared_node",
                args={
                    "source_node_path": source_node_path,
                    "new_node_type": new_node_type,
                    "new_node_name": new_node_name
                },
                description="在 {} 后插入一个共享的 {} 节点，并保持所有下游连接".format(
                    source_node_path,
                    new_node_type
                )
            )
        )

        return plan