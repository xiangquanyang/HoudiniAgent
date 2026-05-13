# -*- coding: utf-8 -*-

from PySide2 import QtWidgets
from PySide2 import QtCore
from ui.llm_worker import PlanBuildWorker

from utils.logger_handler import logger
from controller.agent_controller import AgentController

class AgentWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AgentWindow, self).__init__(parent)
        self.stream_cursor = None
        self.pending_agent_cursor = None
        self.plan_thread = None
        self.plan_worker = None
        self.controller = AgentController()
        self.setWindowTitle("Houdini Agent")
        self.resize(600, 400)
        self.setWindowFlags(
            self.windowFlags() | QtCore.Qt.Tool
        )
        self.build_ui()
        self.create_connections()

    def start_streaming_agent_message(self):
        self.streaming_text = ""
        self.chat_history.append("<b>Agent:</b>")
        self.stream_cursor = self.chat_history.textCursor()
        self.stream_cursor.movePosition(self.stream_cursor.End)

    def append_streaming_token(self, token):
        """对话框中增加流式输出信息"""
        if self.stream_cursor is None:
            self.start_streaming_agent_message()
        safe_token = token.replace("\n", "<br>")
        self.stream_cursor.insertHtml(safe_token)
        self.chat_history.setTextCursor(self.stream_cursor)
        self.chat_history.ensureCursorVisible()

    # 底部状态栏更新
    def set_status(self, status):
        self.status_label.setText(
            "Status: {}".format(status)
        )

    # -------------------------
    # 创建UI
    # -------------------------
    def build_ui(self):

        # 主layout
        self.main_layout = QtWidgets.QVBoxLayout()

        # 聊天记录
        self.chat_history = QtWidgets.QTextBrowser()

        # 输入框
        self.input_edit = QtWidgets.QTextEdit()

        # 按钮
        self.send_button = QtWidgets.QPushButton("Send")

        # 设置输入框高度
        self.input_edit.setFixedHeight(100)

        self.execute_button = QtWidgets.QPushButton("Execute")
        self.execute_button.setEnabled(False)

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setEnabled(False)

        self.clear_memory_button = QtWidgets.QPushButton("Clear Memory")
        self.clear_memory_button.setEnabled(True)

        self.status_label = QtWidgets.QLabel("Status: Ready")


        # 添加到layout
        self.main_layout.addWidget(self.chat_history)
        self.main_layout.addWidget(self.input_edit)
        self.main_layout.addWidget(self.send_button)
        self.main_layout.addWidget(self.execute_button)
        self.main_layout.addWidget(self.cancel_button)
        self.main_layout.addWidget(self.clear_memory_button)
        self.main_layout.addWidget(self.status_label)

        self.setLayout(self.main_layout)

    def add_pending_agent_message(self):
        """添加llm思考时的占位"""
        self.chat_history.append(
            "<b>Agent:思考中...</b>"
        )

    def replace_pending_agent_message(
            self,
            text):
        """llm思考完成后替换之前添加的占位状态"""
        self.chat_history.append(
            "<b>Agent:</b><br>{}".format(
                text.replace("\n", "<br>")
            )
        )

    # -------------------------
    # 信号连接
    # -------------------------
    def create_connections(self):

        self.send_button.clicked.connect(self.on_send_clicked)
        self.execute_button.clicked.connect(self.on_execute_clicked)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)
        self.clear_memory_button.clicked.connect(self.on_clear_clicked)

    # -------------------------
    # 点击发送
    # -------------------------
    # def on_send_clicked(self):
    #
    #     # 获取用户输入
    #     text = self.input_edit.toPlainText()
    #     # 去除首尾空格
    #     text = text.strip()
    #
    #     # 空输入直接返回
    #     if not text:
    #         return
    #
    #     # 显示到聊天记录
    #     self.chat_history.append(
    #         "<b>User:</b> {}".format(text)
    #     )
    #     logger.info(f"用户输入：{text}")
    #     self.set_status("Building Plan")
    #     # 调用Controller
    #     result = self.controller.build_plan(text)
    #     # 更新状态栏
    #     if result["success"]:
    #         self.set_status("Pending Plan")
    #     else:
    #         self.set_status("Failed")
    #     response = result["message"]
    #     safe_response = response.replace("\n", "<br>")
    #     self.chat_history.append(
    #         "<b>Agent:</b><br>{}".format(safe_response)
    #     )
    #     self.execute_button.setEnabled(result["success"])
    #     self.cancel_button.setEnabled(result["success"])
    #     logger.info(f"Agent回复：{response}")
    #     # 清空输入框
    #     self.input_edit.clear()
    def on_send_clicked(self):
        text = self.input_edit.toPlainText().strip()
        if not text:
            return
        self.chat_history.append(
            "<b>User:</b> {}".format(text)
        )
        self.add_pending_agent_message()
        # self.start_streaming_agent_message()
        self.input_edit.clear()
        self.set_status("Building Plan")
        self.send_button.setEnabled(False)
        self.execute_button.setEnabled(False)
        self.cancel_button.setEnabled(False)

        self.on_agent_status_received(
            "正在分析当前场景..."
        )
        context = self.controller.build_scene_context()
        self.start_build_plan_thread(
            text,
            context
        )

    def on_streaming_token_received(self, token):
        """stream方式调用收到返回结果"""
        self.append_streaming_token(token)

    def on_agent_status_received(self, status):
        self.chat_history.append(
            "<span style='color:gray;'>"
            "Agent: {}"
            "</span>".format(status)
        )

    def start_build_plan_thread(self, text, context):
        """创建子线程，绑定agent.run到子线程任务中执行，绑定执行后各种信号的回调函数"""
        self.plan_thread = QtCore.QThread(self)
        self.plan_worker = PlanBuildWorker(
            self.controller,
            text,
            context
        )

        self.plan_worker.status_received.connect(
            self.on_agent_status_received
        )

        self.plan_worker.moveToThread(
            self.plan_thread
        )

        self.plan_thread.started.connect(
            self.plan_worker.run
        )

        self.plan_worker.finished.connect(
            self.on_plan_build_finished
        )

        self.plan_worker.failed.connect(
            self.on_plan_build_failed
        )

        self.plan_worker.finished.connect(
            self.plan_thread.quit
        )

        self.plan_worker.failed.connect(
            self.plan_thread.quit
        )

        self.plan_thread.finished.connect(
            self.plan_worker.deleteLater
        )

        self.plan_thread.finished.connect(
            self.plan_thread.deleteLater
        )

        self.plan_thread.start()

    def on_plan_build_finished(self, result):
        """执行完成后的回调"""
        response = result.get(
            "message",
            "没有返回内容"
        )
        safe_response = response.replace(
            "\n",
            "<br>"
        )
        self.chat_history.append(
            "<b>Plan Preview:</b><br>{}".format(
                safe_response
            )
        )
        success = result.get("success", False)
        self.execute_button.setEnabled(success)
        self.cancel_button.setEnabled(success)
        self.send_button.setEnabled(True)
        if success:
            self.set_status("Pending Plan")
        else:
            self.set_status("Failed")

    def on_plan_build_failed(self, error_message):
        """执行失败的回调"""
        self.replace_pending_agent_message(
            "错误：{}".format(error_message)
        )
        self.send_button.setEnabled(True)
        self.execute_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        self.set_status("Failed")

    # -------------------------
    # 点击执行
    # -------------------------
    def on_execute_clicked(self):
        self.set_status("Executing")
        result = self.controller.execute_pending_plan()
        if result["success"]:
            self.set_status("Executed")
        else:
            self.set_status("Failed")
        response = result["message"]
        safe_response = response.replace("\n", "<br>")
        self.chat_history.append(
            "<b>Agent:</b><br>{}".format(safe_response)
        )
        self.execute_button.setEnabled(False)
        self.cancel_button.setEnabled(False)

    # -------------------------
    # 点击取消
    # -------------------------
    def on_cancel_clicked(self):
        result = self.controller.cancel_pending_plan()
        if result["success"]:
            self.set_status("Cancelled")
        else:
            self.set_status("Ready")
        response = result["message"]
        safe_response = response.replace("\n", "<br>")

        self.chat_history.append(
            "<b>Agent:</b><br>{}".format(safe_response)
        )

        self.execute_button.setEnabled(False)
        self.cancel_button.setEnabled(False)

    def on_clear_clicked(self):
        self.controller.clear_memory()