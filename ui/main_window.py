# -*- coding: utf-8 -*-

from PySide2 import QtWidgets
from PySide2 import QtCore

from utils.logger_handler import logger
from controller.agent_controller import AgentController

class AgentWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AgentWindow, self).__init__(parent)
        self.controller = AgentController()
        self.setWindowTitle("Houdini Agent")
        self.resize(600, 400)
        self.setWindowFlags(
            self.windowFlags() | QtCore.Qt.Tool
        )
        self.build_ui()
        self.create_connections()

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

        self.status_label = QtWidgets.QLabel("Status: Ready")


        # 添加到layout
        self.main_layout.addWidget(self.chat_history)
        self.main_layout.addWidget(self.input_edit)
        self.main_layout.addWidget(self.send_button)
        self.main_layout.addWidget(self.execute_button)
        self.main_layout.addWidget(self.cancel_button)
        self.main_layout.addWidget(self.status_label)

        self.setLayout(self.main_layout)

    # -------------------------
    # 信号连接
    # -------------------------
    def create_connections(self):

        self.send_button.clicked.connect(self.on_send_clicked)
        self.execute_button.clicked.connect(self.on_execute_clicked)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)

    # -------------------------
    # 点击发送
    # -------------------------
    def on_send_clicked(self):

        # 获取用户输入
        text = self.input_edit.toPlainText()
        # 去除首尾空格
        text = text.strip()

        # 空输入直接返回
        if not text:
            return

        # 显示到聊天记录
        self.chat_history.append(
            "<b>User:</b> {}".format(text)
        )
        logger.info(f"用户输入：{text}")
        self.set_status("Building Plan")
        # 调用Controller
        result = self.controller.build_plan(text)
        # 更新状态栏
        if result["success"]:
            self.set_status("Pending Plan")
        else:
            self.set_status("Failed")
        response = result["message"]
        safe_response = response.replace("\n", "<br>")
        self.chat_history.append(
            "<b>Agent:</b><br>{}".format(safe_response)
        )
        self.execute_button.setEnabled(result["success"])
        self.cancel_button.setEnabled(result["success"])
        logger.info(f"Agent回复：{response}")
        # 清空输入框
        self.input_edit.clear()

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