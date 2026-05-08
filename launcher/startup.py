# -*- coding: utf-8 -*-

import hou

from ui.main_window import AgentWindow


window_instance = None


def show_agent():

    global window_instance
    # 关闭旧窗口
    try:
        if window_instance is not None:
            window_instance.close()
            window_instance.deleteLater()
    except:
        pass
    parent = hou.qt.mainWindow()

    window_instance = AgentWindow(parent)

    window_instance.show()
    window_instance.raise_()
    window_instance.activateWindow()