#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志模块 - 支持GUI实时显示、文件和控制台输出
"""

import os
import logging
import datetime
from typing import Optional, List

from PySide6.QtCore import QObject, Signal


class LogSignal(QObject):
    """日志信号类，用于向GUI发送日志消息"""
    new_log = Signal(str, str)  # 参数：日志级别，日志消息


class GuiLogHandler(logging.Handler):
    """自定义日志处理器，将日志发送到GUI"""

    def __init__(self, signal: LogSignal):
        super().__init__()
        self.signal = signal
        self.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

    def emit(self, record):
        """发送日志记录到GUI"""
        msg = self.format(record)
        self.signal.new_log.emit(record.levelname, msg)


class Logger:
    """
    日志管理类 - 支持GUI实时显示和文件、控制台输出
    """

    LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    def __init__(self, name: str = "PySideApp", log_dir: str = "logs",
                 console: bool = True, file: bool = True, gui: bool = False,
                 level: str = "info"):
        """
        初始化日志管理器

        Args:
            name: 日志器名称
            log_dir: 日志文件目录
            console: 是否输出到控制台
            file: 是否输出到文件
            gui: 是否输出到GUI
            level: 日志级别 (debug, info, warning, error, critical)
        """
        self.name = name
        self.log_dir = log_dir
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.LEVELS.get(level.lower(), logging.INFO))
        self.logger.propagate = False

        # 清除现有的处理器
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 添加控制台处理器
        if console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        # 添加文件处理器
        if file:
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            # 以日期命名日志文件
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            log_file = os.path.join(log_dir, f"{name}_{today}.log")

            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        # GUI信号
        self.log_signal = LogSignal() if gui else None

        # 添加GUI处理器
        if gui and self.log_signal:
            gui_handler = GuiLogHandler(self.log_signal)
            self.logger.addHandler(gui_handler)

    def set_level(self, level: str):
        """设置日志级别"""
        self.logger.setLevel(self.LEVELS.get(level.lower(), logging.INFO))

    def debug(self, message: str):
        """记录调试级别日志"""
        self.logger.debug(message)

    def info(self, message: str):
        """记录信息级别日志"""
        self.logger.info(message)

    def warning(self, message: str):
        """记录警告级别日志"""
        self.logger.warning(message)

    def error(self, message: str):
        """记录错误级别日志"""
        self.logger.error(message)

    def critical(self, message: str):
        """记录严重错误级别日志"""
        self.logger.critical(message)

    def get_signal(self) -> Optional[LogSignal]:
        """获取日志信号对象，用于连接到GUI"""
        return self.log_signal