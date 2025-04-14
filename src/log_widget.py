#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志显示组件模块
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QComboBox, QLabel, QCheckBox
)
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QColor, QTextCharFormat, QFont, QTextCursor

from src.logger import Logger, LogSignal


class LogWidget(QWidget):
    """日志显示组件"""

    # 日志级别对应的颜色
    LOG_COLORS = {
        "DEBUG": QColor(128, 128, 128),  # 灰色
        "INFO": QColor(0, 0, 0),         # 黑色
        "WARNING": QColor(255, 165, 0),  # 橙色
        "ERROR": QColor(255, 0, 0),      # 红色
        "CRITICAL": QColor(128, 0, 128)  # 紫色
    }

    def __init__(self, logger: Logger, parent=None):
        """
        初始化日志显示组件

        Args:
            logger: 日志管理器
            parent: 父窗口
        """
        super().__init__(parent)
        self.logger = logger

        # 获取日志信号
        log_signal = logger.get_signal()
        if log_signal:
            log_signal.new_log.connect(self.on_new_log)

        self.setup_ui()

    def setup_ui(self):
        """设置UI界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # 控制区
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 5)

        # 日志级别选择
        level_label = QLabel("日志级别:")
        level_label.setStyleSheet("font-size: 12px;")

        self.level_combo = QComboBox()
        self.level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        self.level_combo.setCurrentText("INFO")
        self.level_combo.setFixedWidth(100)
        self.level_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                padding: 1px 5px;
                background: white;
                font-size: 12px;
            }
        """)
        self.level_combo.currentTextChanged.connect(self.on_level_changed)

        # 自动滚动选项
        self.auto_scroll = QCheckBox("自动滚动")
        self.auto_scroll.setChecked(True)
        self.auto_scroll.setStyleSheet("font-size: 12px;")

        # 添加到控制布局
        control_layout.addWidget(level_label)
        control_layout.addWidget(self.level_combo)
        control_layout.addStretch()
        control_layout.addWidget(self.auto_scroll)

        # 日志显示区域
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.log_text.setStyleSheet("""
            QTextEdit {
                border: none;
                background-color: #f9f9f9;
                font-family: Consolas, monospace;
                font-size: 12px;
                line-height: 1.5;
                padding: 5px;
            }
        """)

        # 设置字体
        font = QFont("Consolas", 9)
        self.log_text.setFont(font)

        # 添加到主布局
        layout.addLayout(control_layout)
        layout.addWidget(self.log_text)

    @Slot(str, str)
    def on_new_log(self, level: str, message: str):
        """
        接收并显示新日志

        Args:
            level: 日志级别
            message: 日志消息
        """
        # 检查当前选择的日志级别是否需要显示
        selected_level = self.level_combo.currentText()
        if Logger.LEVELS.get(level.lower(), 0) < Logger.LEVELS.get(selected_level.lower(), 0):
            return

        # 设置文本颜色
        text_format = QTextCharFormat()
        text_format.setForeground(self.LOG_COLORS.get(level, QColor(0, 0, 0)))

        # 添加日志到文本框
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.setCharFormat(text_format)
        cursor.insertText(message + "\n")

        # 自动滚动到底部
        if self.auto_scroll.isChecked():
            scrollbar = self.log_text.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    @Slot(str)
    def on_level_changed(self, level: str):
        """当日志级别改变时的处理"""
        # 设置日志过滤级别
        self.logger.set_level(level.lower())

    def clear_logs(self):
        """清空日志显示"""
        self.log_text.clear()

    def append_plain_text(self, text: str):
        """添加普通文本到日志显示"""
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(text + "\n")

        # 自动滚动到底部
        if self.auto_scroll.isChecked():
            scrollbar = self.log_text.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())