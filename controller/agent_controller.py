# -*- coding: utf-8 -*-
from agent.fake_agent import FakeAgent
from actions.action_executor import ActionExecutor
from scene.scene_inspector import SceneInspector

class AgentController(object):
    def __init__(self):
        self.agent = FakeAgent()
        self.executor = ActionExecutor()
        self.scene_inspector = SceneInspector()
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