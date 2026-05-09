# -*- coding: utf-8 -*-
from agent.fake_agent import FakeAgent
from actions.action_executor import ActionExecutor
from scene.scene_inspector import SceneInspector

class AgentController(object):
    def __init__(self):
        self.agent = FakeAgent()
        self.executor = ActionExecutor()
        self.scene_inspector = SceneInspector()

        self.pending_plan = None

    # --------------------------------
    # 构建Plan对象
    # --------------------------------
    def build_plan(self, text):
        context = self.scene_inspector.build_context()
        plan = self.agent.run(
            text,
            context
        )
        if plan is None:
            self.pending_plan = None
            return {
                "success": False,
                "message": "无法理解你的请求"
            }
        self.pending_plan = plan
        return {
            "success": True,
            "message": "执行计划：\n{}".format(
                plan.to_preview_text()
            )
        }
    # --------------------------------
    # 执行Plan对象中的Action
    # --------------------------------
    def execute_pending_plan(self):
        if self.pending_plan is None:
            return {
                "success": False,
                "message": "没有待执行的计划"
            }
        results = self.executor.execute_plan(
            self.pending_plan
        )
        success_count = 0
        for result in results:
            if result.get("success"):
                success_count += 1
        total_count = len(results)
        self.pending_plan = None
        return {
            "success": True,
            "message": "执行完成：成功 {}/{} 步".format(
                success_count,
                total_count
            )
        }

    # --------------------------------
    # 处理用户输入
    # --------------------------------
    def process_user_message(self, text):
        # 获取当前场景信息
        context = self.scene_inspector.build_context()
        # --------------------------------
        # Agent生成Plan，Plan中包括若干Action
        # --------------------------------
        plan = self.agent.run(text, context)
        if plan is None:
            return "无法理解你的请求"
        preview_text = plan.to_preview_text()
        # --------------------------------
        # 执行Plan
        # --------------------------------
        results = self.executor.execute_plan(plan)
        success_count = 0
        for result in results:
            if result.get("success"):
                success_count += 1
        return (
            "执行计划：\n{}\n\n"
            "执行完成：成功 {}/{} 步"
        ).format(
            preview_text,
            success_count,
            len(results)
        )