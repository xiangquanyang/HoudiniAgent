# -*- coding: utf-8 -*-
from PySide2 import QtCore

class PlanBuildWorker(QtCore.QObject):
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
            result = self.controller.build_plan_with_context(
                self.text,
                self.context
            )
            self.finished.emit(result)
        except Exception as e:
            self.failed.emit(str(e))