#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主框架实现模块
"""

from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QFontDatabase, QFont

from src.logger import Logger
from src.theme_manager import theme_manager


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

        # 连接主题变更信号
        theme_manager.theme_changed.connect(self._on_theme_changed)

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
        self.setMinimumSize(1000, 800)

        # 设置窗口图标（如果有的话）
        # self.setWindowIcon(QIcon("path/to/icon.png"))

        # 创建中央部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 应用基础样式
        self._update_styles()

    def _update_styles(self):
        """更新样式"""
        colors = theme_manager.get_theme_colors()

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {colors['bg_color']};
            }}
            QLabel {{
                font-size: 13px;
                color: {colors['text_color']};
            }}
            QPushButton {{
                outline: none;
            }}
            QProgressBar {{
                border: none;
                background-color: {colors['progress_bg']};
                border-radius: 3px;
                text-align: center;
            }}
            QProgressBar::chunk {{
                background-color: {colors['progress_fg']};
                border-radius: 3px;
            }}
            QScrollBar:vertical {{
                border: none;
                background: {colors['border_color']};
                width: 8px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {theme_manager._darken_color(colors['border_color'], 0.2)};
                min-height: 20px;
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
            QScrollBar:horizontal {{
                border: none;
                background: {colors['border_color']};
                height: 8px;
                margin: 0px;
            }}
            QScrollBar::handle:horizontal {{
                background: {theme_manager._darken_color(colors['border_color'], 0.2)};
                min-width: 20px;
                border-radius: 4px;
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background: none;
            }}
            QComboBox {{
                border: 1px solid {colors['border_color']};
                border-radius: 3px;
                padding: 2px 5px;
                background: {colors['card_bg']};
                color: {colors['text_color']};
            }}
            QComboBox::drop-down {{
                width: 20px;
                border: none;
            }}
            QCheckBox {{
                spacing: 5px;
                color: {colors['text_color']};
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
            }}
            QTextEdit {{
                border: 1px solid {colors['border_color']};
                border-radius: 3px;
                color: {colors['text_color']};
                background-color: {colors['card_bg']};
            }}
            QToolTip {{
                background-color: {colors['card_bg']};
                color: {colors['text_color']};
                border: 1px solid {colors['border_color']};
                border-radius: 3px;
                padding: 2px;
            }}
            /* 标题栏样式 */
            QMenuBar {{
                background-color: {colors['accent_color']};
                color: white;
                padding: 2px;
            }}
            QMenuBar::item {{
                background-color: transparent;
                padding: 4px 8px;
                border-radius: 3px;
            }}
            QMenuBar::item:selected {{
                background-color: rgba(255, 255, 255, 0.2);
            }}
            QMenuBar::item:pressed {{
                background-color: rgba(255, 255, 255, 0.3);
            }}
            QStatusBar {{
                background-color: {colors['border_color']};
                color: {colors['text_color']};
                border-top: 1px solid {colors['border_color']};
            }}
        """)

    def _on_theme_changed(self, theme_name):
        """主题变更处理函数"""
        self.logger.info(f"应用{theme_name}主题")
        self._update_styles()

    def set_central_layout(self, layout):
        """设置中央布局"""
        self.central_widget.setLayout(layout)

    def closeEvent(self, event):
        """窗口关闭事件"""
        self.logger.info("应用程序关闭")
        event.accept()