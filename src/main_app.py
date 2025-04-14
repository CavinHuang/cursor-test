#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主应用入口模块
"""

import sys
from PySide6.QtWidgets import QApplication, QHBoxLayout

from src.main_frame import MainFrame
from src.navigation.navigation import NavigationSidebar
from src.content.content_pages import ContentManager


def main():
    """应用程序主入口"""
    app = QApplication(sys.argv)

    # 设置应用程序样式
    app.setStyle("Fusion")

    # 创建主窗口
    main_window = MainFrame()

    # 创建导航栏
    sidebar = NavigationSidebar()

    # 创建内容管理器
    content_manager = ContentManager(main_window.logger)

    # 连接导航信号
    sidebar.navigation_changed.connect(content_manager.set_current_page)

    # 创建并设置主布局
    main_layout = QHBoxLayout()
    main_layout.setContentsMargins(0, 0, 0, 0)
    main_layout.setSpacing(0)

    # 添加侧边栏和内容区
    main_layout.addWidget(sidebar)
    main_layout.addWidget(content_manager, 1)  # 内容区可伸展

    # 设置主窗口布局
    main_window.set_central_layout(main_layout)

    # 显示窗口
    main_window.show()

    # 程序入口
    sys.exit(app.exec())


if __name__ == "__main__":
    main()