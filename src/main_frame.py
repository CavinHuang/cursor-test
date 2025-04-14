#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主框架实现模块
"""

from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFontDatabase, QFont

from src.logger import Logger


class MainFrame(QMainWindow):
    """主应用窗口框架"""

    def __init__(self):
        super().__init__()

        # 初始化日志
        self.logger = Logger(
            name="CursorProMax",
            log_dir="logs",
            console=True,
            file=True,
            gui=True,
            level="debug"
        )

        # 设置应用字体
        self._setup_fonts()

        # 设置UI
        self._setup_ui()

        self.logger.info("应用程序框架已初始化")

    def _setup_fonts(self):
        """设置应用字体"""
        # 尝试加载系统字体
        for font_family in ["Microsoft YaHei", "微软雅黑", "SimHei", "黑体", "Arial", "Helvetica"]:
            if font_family in QFontDatabase.families():
                app_font = QFont(font_family)
                app_font.setPointSize(9)  # 设置基础字体大小
                self.setFont(app_font)
                break

    def _setup_ui(self):
        """设置UI框架"""
        self.setWindowTitle("Cursor Pro Max")
        self.setMinimumSize(1000, 700)

        # 设置窗口图标（如果有的话）
        # self.setWindowIcon(QIcon("path/to/icon.png"))

        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 应用基础样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                font-size: 13px;
                color: #333333;
            }
            QPushButton {
                outline: none;
            }
            QProgressBar {
                border: none;
                background-color: #f0f0f0;
                border-radius: 3px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 3px;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar:horizontal {
                border: none;
                background: #f0f0f0;
                height: 8px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #c0c0c0;
                min-width: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
            QComboBox {
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                padding: 2px 5px;
                background: white;
            }
            QComboBox::drop-down {
                width: 20px;
                border: none;
            }
            QCheckBox {
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QTextEdit {
                border: 1px solid #d0d0d0;
                border-radius: 3px;
            }
            QToolTip {
                background-color: #f5f5f5;
                color: #333333;
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                padding: 2px;
            }
            /* 标题栏样式 */
            QMenuBar {
                background-color: #4CAF50;
                color: white;
                padding: 2px;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 4px 8px;
                border-radius: 3px;
            }
            QMenuBar::item:selected {
                background-color: rgba(255, 255, 255, 0.2);
            }
            QMenuBar::item:pressed {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QStatusBar {
                background-color: #f0f0f0;
                color: #333333;
                border-top: 1px solid #d0d0d0;
            }
        """)

    def set_central_layout(self, layout):
        """设置中央布局"""
        self.central_widget.setLayout(layout)

    def closeEvent(self, event):
        """窗口关闭事件"""
        self.logger.info("应用程序关闭")
        event.accept()