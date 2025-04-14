#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
导航组件实现模块
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal


class SidebarButton(QPushButton):
    """侧边栏按钮"""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(40)
        self.setFixedWidth(180)
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 4px;
                color: #333;
                text-align: left;
                padding-left: 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.05);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.1);
            }
            QPushButton:checked {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
        """)
        self.setCheckable(True)


class NavigationSidebar(QWidget):
    """导航侧边栏组件"""

    # 定义导航信号
    navigation_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self.setStyleSheet("""
            background-color: #f0f0f0;
            border-right: 1px solid #e0e0e0;
        """)

        self._setup_ui()

    def _setup_ui(self):
        """设置UI界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(8)

        # 标题
        title = QLabel("CursorProMax")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: #4CAF50;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)

        # 导航按钮区域 - 包装在单独的容器中以更好地控制间距
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(0)  # 按钮之间无间距

        # 导航按钮
        self.btn_home = SidebarButton("主页")
        self.btn_account = SidebarButton("账号管理")
        self.btn_settings = SidebarButton("设置")
        self.btn_about = SidebarButton("关于")

        # 设置默认选中
        self.btn_home.setChecked(True)

        # 连接信号
        self.btn_home.clicked.connect(lambda: self._on_navigation_changed("home"))
        self.btn_account.clicked.connect(lambda: self._on_navigation_changed("account"))
        self.btn_settings.clicked.connect(lambda: self._on_navigation_changed("settings"))
        self.btn_about.clicked.connect(lambda: self._on_navigation_changed("about"))

        # 添加按钮到导航容器
        nav_layout.addWidget(self.btn_home)
        nav_layout.addWidget(self.btn_account)
        nav_layout.addWidget(self.btn_settings)
        nav_layout.addWidget(self.btn_about)

        # 添加导航容器到主布局
        layout.addWidget(nav_container)

        # 添加伸展空间
        layout.addStretch(1)

        # 添加样式切换按钮（参考图最底部的按钮）
        theme_switcher = QPushButton("切换到深色主题")
        theme_switcher.setFixedHeight(30)
        theme_switcher.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
                font-size: 12px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed {
                background-color: #222;
            }
        """)
        theme_switcher.clicked.connect(self._on_theme_switch)
        layout.addWidget(theme_switcher)

    def _on_navigation_changed(self, page_name):
        """导航变更处理函数"""
        # 更新按钮选中状态
        for btn in [self.btn_home, self.btn_account, self.btn_settings, self.btn_about]:
            btn.setChecked(False)

        # 设置当前按钮选中
        if page_name == "home":
            self.btn_home.setChecked(True)
        elif page_name == "account":
            self.btn_account.setChecked(True)
        elif page_name == "settings":
            self.btn_settings.setChecked(True)
        elif page_name == "about":
            self.btn_about.setChecked(True)

        # 发送导航变更信号
        self.navigation_changed.emit(page_name)

    def _on_theme_switch(self):
        """切换主题"""
        # 这里只是一个演示，实际功能需要与全局主题管理结合
        sender = self.sender()
        if sender.text() == "切换到深色主题":
            sender.setText("切换到浅色主题")
        else:
            sender.setText("切换到深色主题")