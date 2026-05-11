# -*- coding: utf-8 -*-
from PySide2 import QtCore

class PlanBuildWorker(QtCore.QObject):
    status_received = QtCore.Signal(str)
    finished = QtCore.Signal(dict)
    failed = QtCore.Signal(str)
    def __init__(self, controller, text, context):
        super(PlanBuildWorker, self).__init__()
        self.controller = controller
        self.text = text
        self.context = context

    @QtCore.Slot()
    def run(self):
        try:
            self.status_received.emit(
                "正在理解用户意图并生成执行计划..."
            )
            result = self.controller.stream_build_plan_with_context(
                self.text,
                self.context,
                on_token=None
            )
            self.status_received.emit("执行计划生成完成")
            self.finished.emit(result)
        except Exception as e:
            self.failed.emit(str(e))

    def on_token(self, token):
        """将传入的token作为token_received信号的值emit出去"""
        self.token_received.emit(token)