#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
导航组件实现模块
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal

from src.theme_manager import theme_manager


class SidebarButton(QPushButton):
    """侧边栏按钮"""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(40)
        self.setFixedWidth(180)
        self._update_style()
        self.setCheckable(True)

        # 连接主题变更信号
        theme_manager.theme_changed.connect(self._on_theme_changed)

    def _update_style(self):
        """更新按钮样式"""
        colors = theme_manager.get_theme_colors()
        current_theme = theme_manager.current_theme

        # 根据主题设置不同的hover和pressed样式
        if current_theme == "dark":
            hover_bg = "rgba(255, 255, 255, 0.1)"  # 深色主题下使用亮色背景
            pressed_bg = "rgba(255, 255, 255, 0.15)"  # 深色主题下使用更亮的背景
        else:
            hover_bg = "rgba(0, 0, 0, 0.05)"  # 浅色主题下使用原有的样式
            pressed_bg = "rgba(0, 0, 0, 0.1)"  # 浅色主题下使用原有的样式

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: 8px;
                color: {colors['nav_text']};
                text-align: left;
                padding-left: 15px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {hover_bg};
            }}
            QPushButton:pressed {{
                background-color: {pressed_bg};
            }}
            QPushButton:checked {{
                background-color: {colors['nav_selected_bg']};
                color: {colors['nav_selected_text']};
                font-weight: bold;
            }}
        """)

    def _on_theme_changed(self, theme_name):
        """主题变更处理函数"""
        self._update_style()


class NavigationSidebar(QWidget):
    """导航侧边栏组件"""

    # 定义导航信号
    navigation_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(200)
        self._update_styles()

        # 连接主题变更信号
        theme_manager.theme_changed.connect(self._on_theme_changed)

        self._setup_ui()

    def _update_styles(self):
        """更新样式"""
        colors = theme_manager.get_theme_colors()
        self.setStyleSheet(f"""
            background-color: {colors['nav_bg']};
            border-right: 1px solid {colors['border_color']};
        """)

    def _on_theme_changed(self, theme_name):
        """主题变更处理函数"""
        self._update_styles()

        # 更新主题切换按钮文本和样式
        if hasattr(self, 'theme_switcher'):
            colors = theme_manager.get_theme_colors()

            if theme_name == "light":
                self.theme_switcher.setText("切换到深色主题")
                # 浅色主题下的样式
                self.theme_switcher.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {colors['accent_color']};
                        color: white;
                        border: none;
                        border-radius: 8px;
                        padding: 5px;
                        font-size: 12px;
                        text-align: center;
                    }}
                    QPushButton:hover {{
                        background-color: {self._lighten_color(colors['accent_color'])};
                    }}
                    QPushButton:pressed {{
                        background-color: {self._darken_color(colors['accent_color'])};
                    }}
                """)
            else:
                self.theme_switcher.setText("切换到浅色主题")
                # 深色主题下的样式
                self.theme_switcher.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {colors['accent_color']};
                        color: #ffffff; /* 确保文本在深色主题下清晰可见 */
                        border: none;
                        border-radius: 8px;
                        padding: 5px;
                        font-size: 12px;
                        text-align: center;
                    }}
                    QPushButton:hover {{
                        background-color: {self._lighten_color(colors['accent_color'], 0.15)}; /* 增加亮度因子 */
                    }}
                    QPushButton:pressed {{
                        background-color: {self._lighten_color(colors['accent_color'], 0.05)};
                    }}
                """)

    def _setup_ui(self):
        """设置UI界面"""
        # 创建一个白色背景的容器作为底层
        colors = theme_manager.get_theme_colors()

        main_container = QWidget(self)
        main_container.setGeometry(0, 0, 200, 9999)  # 设置足够大的高度

        # 根据主题设置不同的容器样式
        if theme_manager.current_theme == "dark":
            main_container.setStyleSheet(f"background-color: {colors['nav_bg']};border: none;")
        else:
            main_container.setStyleSheet(f"background-color: {colors['nav_bg']};border: none;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(8)

        # 标题
        title = QLabel("CursorProMax")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"""
            color: {colors['accent_color']};
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 20px;
            background-color: transparent;
            border: none;
        """)
        layout.addWidget(title)

        # 导航按钮区域 - 包装在单独的容器中以更好地控制间距
        nav_container = QWidget()
        nav_container.setObjectName("nav_container")
        # 根据主题设置导航容器样式
        if theme_manager.current_theme == "dark":
            nav_container.setStyleSheet(f"background-color: {colors['nav_bg']};border: none;")
        else:
            nav_container.setStyleSheet(f"background-color: {colors['nav_bg']};border: none;")
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

        # 底部容器，确保白色背景延伸
        bottom_container = QWidget()
        bottom_container.setObjectName("bottom_container")
        # 根据主题设置底部容器样式
        if theme_manager.current_theme == "dark":
            bottom_container.setStyleSheet(f"background-color: {colors['nav_bg']}; border: none;")
        else:
            bottom_container.setStyleSheet(f"background-color: {colors['nav_bg']}; border: none;")
        bottom_layout = QVBoxLayout(bottom_container)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(5)

        # 添加样式切换按钮
        current_theme = theme_manager.current_theme
        btn_text = "切换到深色主题" if current_theme == "light" else "切换到浅色主题"

        self.theme_switcher = QPushButton(btn_text)
        self.theme_switcher.setFixedHeight(30)

        # 根据当前主题设置不同的按钮样式
        if current_theme == "dark":
            # 深色主题下使用更明显的对比色
            self.theme_switcher.setStyleSheet(f"""
                QPushButton {{
                    background-color: {colors['accent_color']};
                    color: #ffffff; /* 确保文本在深色主题下清晰可见 */
                    border: none;
                    border-radius: 8px;
                    padding: 5px;
                    font-size: 12px;
                    text-align: center;
                }}
                QPushButton:hover {{
                    background-color: {self._lighten_color(colors['accent_color'], 0.15)}; /* 增加亮度因子 */
                }}
                QPushButton:pressed {{
                    background-color: {self._lighten_color(colors['accent_color'], 0.05)};
                }}
            """)
        else:
            # 浅色主题下的样式
            self.theme_switcher.setStyleSheet(f"""
                QPushButton {{
                    background-color: {colors['accent_color']};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 5px;
                    font-size: 12px;
                    text-align: center;
                }}
                QPushButton:hover {{
                    background-color: {self._lighten_color(colors['accent_color'])};
                }}
                QPushButton:pressed {{
                    background-color: {self._darken_color(colors['accent_color'])};
                }}
            """)
        self.theme_switcher.clicked.connect(self._on_theme_switch)
        bottom_layout.addWidget(self.theme_switcher)

        layout.addWidget(bottom_container)

    def _lighten_color(self, color, factor=0.1):
        """使颜色变亮"""
        if color.startswith('#'):
            color = color[1:]
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _darken_color(self, color, factor=0.1):
        """使颜色变暗"""
        if color.startswith('#'):
            color = color[1:]
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r = max(0, int(r * (1 - factor)))
        g = max(0, int(g * (1 - factor)))
        b = max(0, int(b * (1 - factor)))
        return f"#{r:02x}{g:02x}{b:02x}"

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
        # 调用主题管理器切换主题
        theme_manager.switch_theme()