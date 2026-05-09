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

        # 添加到layout
        self.main_layout.addWidget(self.chat_history)
        self.main_layout.addWidget(self.input_edit)
        self.main_layout.addWidget(self.send_button)

        self.setLayout(self.main_layout)

    # -------------------------
    # 信号连接
    # -------------------------
    def create_connections(self):

        self.send_button.clicked.connect(self.on_send_clicked)

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
        # 调用Controller
        response = self.controller.process_user_message(
            text
        )
        safe_response = response.replace("\n", "<br>")
        # 显示Agent回复
        self.chat_history.append(
            "<b>Agent:</b><br>{}".format(safe_response)
        )
        logger.info(f"Agent回复：{response}")
        # 清空输入框
        self.input_edit.clear()