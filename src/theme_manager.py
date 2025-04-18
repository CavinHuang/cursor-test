#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主题管理器模块 - 管理应用程序的主题切换
"""

from PySide6.QtCore import QObject, Signal


class ThemeManager(QObject):
    """主题管理器类"""

    # 主题变更信号
    theme_changed = Signal(str)

    # 主题配色方案
    THEMES = {
        "light": {
            "bg_color": "#f5f5f5",
            "card_bg": "#ffffff",
            "text_color": "#333333",
            "border_color": "#e0e0e0",
            "accent_color": "#4CAF50",
            "progress_bg": "#e8e8e8",
            "progress_fg": "#4CAF50",
            "btn_text": "#ffffff",
            "section_bg": "#ffffff",
            "nav_bg": "#ffffff",
            "nav_text": "#333333",
            "nav_selected_bg": "#4CAF50",
            "nav_selected_text": "#ffffff",
            "refresh_btn_bg": "#f0f0f0",
            "refresh_btn_hover": "#e0e0e0",
            "refresh_btn_pressed": "#d0d0d0",
            "refresh_btn_text": "#333",
        },
        "dark": {
            "bg_color": "#1e1e1e",
            "card_bg": "#252525",
            "text_color": "#e0e0e0",
            "border_color": "#333333",
            "accent_color": "#4CAF50",
            "progress_bg": "#383838",
            "progress_fg": "#4CAF50",
            "btn_text": "#ffffff",
            "section_bg": "#252525",
            "nav_bg": "#252525",
            "nav_text": "#e0e0e0",
            "nav_selected_bg": "#4CAF50",
            "nav_selected_text": "#ffffff",
            "dark_log_bg": "#1a1a1a",   # 日志背景更暗
            "dark_text": "#bbbbbb",     # 次要文本颜色
            "dark_border": "#333333",   # 深色边框
            "refresh_btn_bg": "#1a1a1a",
            "refresh_btn_hover": "#252525",
            "refresh_btn_pressed": "#383838",
            "refresh_btn_text": "#e0e0e0",
        }
    }

    def __init__(self):
        super().__init__()
        self._current_theme = "light"  # 默认为亮色主题

    @property
    def current_theme(self):
        """获取当前主题名称"""
        return self._current_theme

    def get_theme_colors(self):
        """获取当前主题的颜色配置"""
        return self.THEMES.get(self._current_theme, self.THEMES["light"])

    def switch_theme(self):
        """切换主题"""
        if self._current_theme == "light":
            self._current_theme = "dark"
        else:
            self._current_theme = "light"

        # 发送主题变更信号
        self.theme_changed.emit(self._current_theme)

        return self._current_theme

    def set_theme(self, theme_name):
        """设置特定主题"""
        if theme_name in self.THEMES:
            self._current_theme = theme_name
            self.theme_changed.emit(self._current_theme)
            return True
        return False

    @staticmethod
    def _lighten_color(color, factor=0.1):
        """使颜色变亮"""
        if color.startswith('#'):
            color = color[1:]
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def _darken_color(color, factor=0.1):
        """使颜色变暗"""
        if color.startswith('#'):
            color = color[1:]
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r = max(0, int(r * (1 - factor)))
        g = max(0, int(g * (1 - factor)))
        b = max(0, int(b * (1 - factor)))
        return f"#{r:02x}{g:02x}{b:02x}"


# 创建全局实例
theme_manager = ThemeManager()