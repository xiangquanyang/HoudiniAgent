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
        print("=" * 50)
        print("Scene Context:")
        print(context.to_dict())
        # --------------------------------
        # Agent生成Plan，Plan中包括若干Action
        # --------------------------------
        plan = self.agent.run(text, context)
        if plan is None:
            return "无法理解你的请求"
        # --------------------------------
        # 执行Plan
        # --------------------------------
        results = self.executor.execute_plan(plan)
        return "执行完成"