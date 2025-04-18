#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
内容页面模块 - 包含各页面的实现
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QFrame, QTextEdit, QStackedWidget, QSplitter, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QFont, QColor

from src.logger import Logger
from src.log_widget import LogWidget
from src.theme_manager import theme_manager


class RoundedButton(QPushButton):
    """圆角按钮"""

    def __init__(self, text, color="#6200ee", parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(44)
        self.setMinimumWidth(100)
        self.color = color
        self._update_style()

        # 连接主题变更信号
        theme_manager.theme_changed.connect(self._on_theme_changed)

    def _update_style(self):
        """更新按钮样式"""
        # 暗黑模式下按钮稍微调暗一些，使其颜色不那么刺眼
        current_color = self.color
        if theme_manager.current_theme == "dark":
            # 使颜色暗一些但保持色调
            current_color = self._adjust_color_for_dark(self.color)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {current_color};
                border: none;
                border-radius: 22px;
                color: white;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {self._lighten_color(current_color, 0.1)};
            }}
            QPushButton:pressed {{
                background-color: {self._darken_color(current_color, 0.1)};
            }}
        """)

    def _on_theme_changed(self, theme_name):
        """主题变更时更新样式"""
        self._update_style()

    def _adjust_color_for_dark(self, color, factor=0.8):
        """调整颜色适应暗黑模式"""
        if color.startswith('#'):
            color = color[1:]
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        # 降低亮度但保持色调
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        return f"#{r:02x}{g:02x}{b:02x}"

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


class InfoPanel(QWidget):
    """信息面板组件"""

    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            background-color: white;
            border-radius: 8px;
            padding: 10px;
            margin: 5px;
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(8)

        # 标题
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight: bold;")
        self.layout.addWidget(self.title_label)

    def add_widget(self, widget):
        """添加部件到面板"""
        self.layout.addWidget(widget)

    def add_layout(self, layout):
        """添加布局到面板"""
        self.layout.addLayout(layout)

    def add_refresh_button(self, callback):
        """添加刷新按钮"""
        refresh_button = QPushButton("刷新")
        refresh_button.setFixedSize(60, 30)
        refresh_button.clicked.connect(callback)
        self.layout.addWidget(refresh_button, 0, Qt.AlignRight)


class HomePage(QWidget):
    """主页内容"""

    def __init__(self, logger: Logger, parent=None):
        super().__init__(parent)
        self.logger = logger

        # 初始化UI
        self._setup_ui()

        # 连接主题切换信号
        theme_manager.theme_changed.connect(self._on_theme_changed)

    def _setup_ui(self):
        """设置UI"""
        # 整体布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)

        # 获取当前主题颜色
        colors = theme_manager.get_theme_colors()

        # 设置主页面背景色
        self.setStyleSheet(f"background-color: {colors['bg_color']};")

        # 顶部描述区域
        description_widget = QWidget()
        description_widget.setObjectName("description_widget")
        description_widget.setStyleSheet(f"""
            background-color: {colors['section_bg']};
            border-radius: 4px;
            border: none;
        """)
        description_layout = QVBoxLayout(description_widget)
        description_layout.setContentsMargins(12, 12, 12, 12)
        description_layout.setSpacing(8)  # 两行之间的间距

        # 第一行描述
        bullet_point1 = QLabel("•")
        desc1 = QLabel("「Cursor Pro Max」是一个完全免费的工具，仅供个人学习和研究使用")
        bullet_point1.setStyleSheet(f"font-size: 14px; color: {colors['text_color']}; font-weight: bold; border: none;")
        desc1.setStyleSheet(f"font-size: 13px; color: {colors['text_color']}; border: none;")

        bullet_layout1 = QHBoxLayout()
        bullet_layout1.setContentsMargins(0, 0, 0, 0)
        bullet_layout1.setSpacing(6)  # 项目符号和文本之间的间距
        bullet_layout1.addWidget(bullet_point1)
        bullet_layout1.addWidget(desc1)
        bullet_layout1.addStretch()

        # 第二行描述
        bullet_point2 = QLabel("•")
        desc2 = QLabel("更多资源请关注微信公众号")
        bullet_point2.setStyleSheet(f"font-size: 14px; color: {colors['text_color']}; font-weight: bold;border: none;")
        desc2.setStyleSheet(f"font-size: 13px; color: {colors['text_color']}; border: none;")

        bullet_layout2 = QHBoxLayout()
        bullet_layout2.setContentsMargins(0, 0, 0, 0)
        bullet_layout2.setSpacing(6)  # 项目符号和文本之间的间距
        bullet_layout2.addWidget(bullet_point2)
        bullet_layout2.addWidget(desc2)
        bullet_layout2.addStretch()

        description_layout.addLayout(bullet_layout1)
        description_layout.addLayout(bullet_layout2)
        main_layout.addWidget(description_widget)

        # 顶部信息区域 - 两个卡片
        top_layout = QHBoxLayout()
        top_layout.setSpacing(12)  # 两个卡片之间的间距

        # 系统信息卡片
        sys_info_panel = QWidget()
        sys_info_panel.setObjectName("sys_info_panel")
        sys_info_panel.setStyleSheet(f"""
            background-color: {colors['card_bg']};
            border-radius: 4px;
            border: none;
        """)
        sys_info_layout = QVBoxLayout(sys_info_panel)
        sys_info_layout.setContentsMargins(12, 12, 12, 12)
        sys_info_layout.setSpacing(12)  # 紧凑的行间距

        # 标题和刷新按钮并排
        sys_header_layout = QHBoxLayout()
        sys_header_layout.setContentsMargins(0, 0, 0, 0)
        sys_header_layout.setSpacing(0)

        sys_title = QLabel("系统信息")
        sys_title.setStyleSheet(f"font-weight: bold; font-size: 13px; color: {colors['text_color']};")

        refresh_sys_btn = QPushButton("刷新")
        refresh_sys_btn.setFixedSize(50, 24)

        refresh_sys_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['refresh_btn_bg']};
                border: none;
                border-radius: 2px;
                padding: 2px;
                font-size: 12px;
                color: {colors['refresh_btn_text']};
            }}
            QPushButton:hover {{
                background-color: {colors['refresh_btn_hover']};
            }}
            QPushButton:pressed {{
                background-color: {colors['refresh_btn_pressed']};
            }}
        """)
        refresh_sys_btn.clicked.connect(lambda: self.logger.info("刷新系统信息"))

        sys_header_layout.addWidget(sys_title)
        sys_header_layout.addStretch()
        sys_header_layout.addWidget(refresh_sys_btn)
        sys_info_layout.addLayout(sys_header_layout)

        # 系统信息内容
        chrome_version = QLabel("Chrome版本: 135.0.7049.85")
        cursor_version = QLabel("Cursor版本: 0.48.7")
        os_version = QLabel("操作系统: Windows 10")

        chrome_version.setStyleSheet(f"font-size: 13px; color: {colors['text_color']}; border: none;")
        cursor_version.setStyleSheet(f"font-size: 13px; color: {colors['text_color']}; border: none;")
        os_version.setStyleSheet(f"font-size: 13px; color: {colors['text_color']}; border: none;")

        sys_info_layout.addWidget(chrome_version)
        sys_info_layout.addWidget(cursor_version)
        sys_info_layout.addWidget(os_version)
        sys_info_layout.addStretch()  # 确保内容顶部对齐

        # 账号状态卡片
        account_panel = QWidget()
        account_panel.setObjectName("account_panel")
        account_panel.setStyleSheet(f"""
            background-color: {colors['card_bg']};
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        """)
        account_layout = QVBoxLayout(account_panel)
        account_layout.setContentsMargins(20, 20, 20, 20)
        account_layout.setSpacing(12)  # 增加间距使布局更宽松

        # 标题和刷新按钮并排
        account_header_layout = QHBoxLayout()
        account_header_layout.setContentsMargins(0, 0, 0, 5)
        account_header_layout.setSpacing(0)

        account_title = QLabel("本地账号状态")
        account_title.setStyleSheet("font-weight: bold; font-size: 14px;")

        refresh_account_btn = QPushButton("刷新")
        refresh_account_btn.setFixedSize(50, 24)

        refresh_account_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['refresh_btn_bg']};
                border: none;
                border-radius: 2px;
                padding: 2px;
                font-size: 12px;
                color: {colors['text_color']};
            }}
            QPushButton:hover {{
                background-color: {colors['refresh_btn_hover']};
            }}
            QPushButton:pressed {{
                background-color: {colors['refresh_btn_pressed']};
            }}
        """)
        refresh_account_btn.clicked.connect(lambda: self.logger.info("刷新账号状态"))

        account_header_layout.addWidget(account_title)
        account_header_layout.addStretch()
        account_header_layout.addWidget(refresh_account_btn)
        account_layout.addLayout(account_header_layout)

        # 账号状态内容 - 与图片一致
        account_status = QLabel("账号状态: 账户状态正常 (登录类型: AUTH_0)")
        member_type = QLabel("会员类型: 免费试用")
        remain_days = QLabel("剩余天数: 7")
        usage_label = QLabel("使用量: 26/150")

        # 设置统一字体大小和样式，图片中的字体大小一致
        account_status.setStyleSheet("font-size: 14px; margin-top: 4px;")
        member_type.setStyleSheet("font-size: 14px; margin-top: 4px;")
        remain_days.setStyleSheet("font-size: 14px; margin-top: 4px;")
        usage_label.setStyleSheet("font-size: 14px;")

        account_layout.addWidget(account_status)
        account_layout.addWidget(member_type)
        account_layout.addWidget(remain_days)

        # 为使用量和进度条创建更清晰的结构
        usage_section = QWidget()
        usage_layout = QVBoxLayout(usage_section)
        usage_layout.setContentsMargins(0, 8, 0, 5)  # 添加上下间距
        usage_layout.setSpacing(8)  # 组件之间的间距

        usage_layout.addWidget(usage_label)

        # 进度条 - 匹配图片样式
        self.usage_bar = QProgressBar()
        self.usage_bar.setRange(0, 150)
        self.usage_bar.setValue(26)
        self.usage_bar.setFixedHeight(8)  # 增加高度确保可见
        self.usage_bar.setTextVisible(False)
        self.usage_bar.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                background-color: #f0f0f0;
                border-radius: 4px;
                min-height: 8px;
            }}
            QProgressBar::chunk {{
                background-color: #4c6cf5;
                border-radius: 4px;
            }}
        """)

        account_layout.addWidget(usage_section)
        account_layout.addStretch(1)  # 在底部添加伸展空间

        # 添加到顶部布局
        top_layout.addWidget(sys_info_panel, 1)  # 1:1比例
        top_layout.addWidget(account_panel, 1)   # 1:1比例

        main_layout.addLayout(top_layout)

        # 操作按钮区域 - 五个彩色按钮
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(0, 10, 0, 10)
        buttons_layout.setSpacing(8)  # 按钮之间的间距

        # 更精确匹配参考图的按钮颜色和尺寸
        btn_register = RoundedButton("仅注册账号", "#7061e3")  # 紫色调整
        btn_reset = RoundedButton("仅重置机器", "#4c6cf5")     # 蓝紫色调整
        btn_register_reset = RoundedButton("一键注册重置", "#ff7043")  # 橙红色
        btn_switch = RoundedButton("随机切换账号", "#00bfa5")  # 青绿色
        btn_close = RoundedButton("关闭浏览器", "#2c3e50")     # 深蓝灰色

        # 自定义每个按钮的样式
        for btn in [btn_register, btn_reset, btn_register_reset, btn_switch, btn_close]:
            btn.setFixedHeight(44)  # 固定高度

        btn_register.clicked.connect(lambda: self._on_button_clicked("仅注册账号"))
        btn_reset.clicked.connect(lambda: self._on_button_clicked("仅重置机器"))
        btn_register_reset.clicked.connect(lambda: self._on_button_clicked("一键注册重置"))
        btn_switch.clicked.connect(lambda: self._on_button_clicked("随机切换账号"))
        btn_close.clicked.connect(lambda: self._on_button_clicked("关闭浏览器"))

        buttons_layout.addWidget(btn_register)
        buttons_layout.addWidget(btn_reset)
        buttons_layout.addWidget(btn_register_reset)
        buttons_layout.addWidget(btn_switch)
        buttons_layout.addWidget(btn_close)

        main_layout.addLayout(buttons_layout)

        # 日志区域
        logs_panel = QWidget()
        logs_panel.setObjectName("logs_panel")
        logs_panel.setStyleSheet(f"""
            background-color: {colors['card_bg']};
            border-radius: 4px;
            border: 1px solid {colors['border_color']};
        """)
        logs_layout = QVBoxLayout(logs_panel)
        logs_layout.setContentsMargins(12, 12, 12, 12)
        logs_layout.setSpacing(5)

        # 日志标题栏
        log_header = QHBoxLayout()
        log_header.setContentsMargins(0, 0, 0, 6)
        log_header.setSpacing(10)

        log_title = QLabel("日志输出")
        log_title.setStyleSheet(f"font-weight: bold; font-size: 13px; color: {colors['text_color']}; border: none;")

        log_header.addWidget(log_title)
        log_header.addStretch(1)

        # 清空和打开按钮
        btn_clear = QPushButton("清空显示区域")
        btn_clear.setFixedSize(100, 26)
        btn_clear.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['refresh_btn_bg']};
                color: {colors['refresh_btn_text']};
                border: none;
                border-radius: 3px;
                padding: 3px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {colors['refresh_btn_hover']};
            }}
            QPushButton:pressed {{
                background-color: {colors['refresh_btn_pressed']};
            }}
        """)
        btn_clear.clicked.connect(self._on_clear_logs)

        btn_open_file = QPushButton("打开日志文件")
        btn_open_file.setFixedSize(100, 26)
        btn_open_file.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['refresh_btn_bg']};
                color: {colors['text_color']};
                border: none;
                border-radius: 3px;
                padding: 3px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {colors['refresh_btn_hover']};
            }}
            QPushButton:pressed {{
                background-color: {colors['refresh_btn_pressed']};
            }}
        """)
        btn_open_file.clicked.connect(self._on_open_log_file)

        log_header.addWidget(btn_clear)
        log_header.addWidget(btn_open_file)

        logs_layout.addLayout(log_header)

        # 精确匹配参考图的日志文本
        sample_text = QTextEdit()
        sample_text.setReadOnly(True)
        sample_text.setContentsMargins(0, 6, 0, 6)
        dark_log_bg = colors.get('dark_log_bg', '#1a1a1a') if theme_manager.current_theme == 'dark' else colors['section_bg']
        sample_text.setStyleSheet(f"""
            QTextEdit {{
                border: none;
                background-color: {dark_log_bg};
                color: {colors['text_color']};
                font-family: Consolas, monospace;
                font-size: 12px;
                line-height: 1.3;
                padding: 5px;
            }}
        """)

        # 精确匹配参考图中的文本内容
        log_content = """邮箱: gcj1c4gy16378668terminalxp.site
密码: 63lwe#p9Yxce

账号状态: 账户状态正常 (登录类型: AUTH_0)
会员类型: 免费试用
剩余天数: 14

模型: gpt-4
本月已使用次数: 0 次
本月可用总次数: 150 次
注册账号执行成功
未预创建token或路径自定义的路径为空，尝试使用默认认证
使用认证路径控制配置: C:\\Users\\A\\AppData\\Roaming\\Cursor\\User\\globalStorage\\state.vscdb
已获取到账号: aric07@jingxcai.site
用户ID: user_01JR8GRE9VP2J9OVDSYTTBPBH1
未预创建token或路径自定义的路径为空，尝试使用默认认证
使用认证路径控制: package.json: C:\\Users\\A\\AppData\\Local\\Programs\\cursor\\resources\\app\\package.json
获取到的 Cursor 版本: 0.48.7"""

        sample_text.setPlainText(log_content)
        sample_text.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        logs_layout.addWidget(sample_text, 1)  # 让日志文本区域可扩展

        main_layout.addWidget(logs_panel, 1)  # 让日志区域可扩展

    def _on_theme_changed(self, theme_name):
        """主题变更处理函数"""
        self.logger.info(f"切换到{theme_name}主题")

        # 获取新主题的颜色
        colors = theme_manager.get_theme_colors()

        # 更新主页面背景色
        self.setStyleSheet(f"background-color: {colors['bg_color']};")

        # 更新描述区域
        for widget in self.findChildren(QWidget):
            if hasattr(widget, 'objectName') and widget.objectName() == "description_widget":
                widget.setStyleSheet(f"""
                    background-color: {colors['section_bg']};
                    border-radius: 4px;
                    border: none;
                """)
            elif hasattr(widget, 'objectName') and widget.objectName() == "sys_info_panel":
                widget.setStyleSheet(f"""
                    background-color: {colors['card_bg']};
                    border-radius: 4px;
                    border: none;
                """)
            elif hasattr(widget, 'objectName') and widget.objectName() == "account_panel":
                widget.setStyleSheet(f"""
                    background-color: {colors['card_bg']};
                    border-radius: 8px;
                    border: none;
                """)
            elif hasattr(widget, 'objectName') and widget.objectName() == "logs_panel":
                widget.setStyleSheet(f"""
                    background-color: {colors['card_bg']};
                    border-radius: 4px;
                    border: none;
                """)

        # 更新文本颜色
        for label in self.findChildren(QLabel):
            if label.text() == "•":
                label.setStyleSheet(f"font-size: 14px; color: {colors['text_color']}; font-weight: bold;")
            elif not hasattr(label, 'objectName') or not label.objectName().startswith("title_"):
                label.setStyleSheet(f"color: {colors['text_color']}; font-size: 13px;")

        # 更新按钮样式
        for btn in self.findChildren(QPushButton):
            if not isinstance(btn, RoundedButton) and not hasattr(btn, 'objectName') or (hasattr(btn, 'objectName') and btn.objectName().startswith("btn_")):

                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {colors['refresh_btn_bg']};
                        color: {colors['text_color']};
                        border: none;
                        border-radius: 3px;
                        padding: 3px;
                        font-size: 12px;
                    }}
                    QPushButton:hover {{
                        background-color: {colors['refresh_btn_hover']};
                    }}
                    QPushButton:pressed {{
                        background-color: {colors['refresh_btn_pressed']};
                    }}
                """)

        # 更新进度条颜色
        if hasattr(self, 'usage_bar'):
            self.usage_bar.setStyleSheet(f"""
                QProgressBar {{
                    border: none;
                    background-color: {colors['progress_bg']};
                    border-radius: 3px;
                    min-height: 6px;
                }}
                QProgressBar::chunk {{
                    background-color: {colors['progress_fg']};
                    border-radius: 3px;
                }}
            """)

        # 更新文本编辑区域
        for text_edit in self.findChildren(QTextEdit):
            dark_log_bg = colors.get('dark_log_bg', '#1a1a1a') if theme_name == 'dark' else colors['section_bg']
            text_edit.setStyleSheet(f"""
                QTextEdit {{
                    border: none;
                    background-color: {dark_log_bg};
                    color: {colors['text_color']};
                    font-family: Consolas, monospace;
                    font-size: 12px;
                    line-height: 1.3;
                    padding: 5px;
                }}
            """)

    def _on_button_clicked(self, button_name):
        """处理按钮点击事件"""
        self.logger.info(f"点击了按钮: {button_name}")

        # 模拟一些操作
        if button_name == "仅注册账号":
            self.logger.info("开始注册账号...")
            self.logger.warning("注册过程可能需要一段时间")
        elif button_name == "仅重置机器":
            self.logger.info("正在重置机器...")
        elif button_name == "一键注册重置":
            self.logger.info("执行一键注册重置...")
            self.logger.warning("此操作将重置所有信息")
        elif button_name == "随机切换账号":
            self.logger.info("正在随机切换账号...")
            self.logger.debug("检查可用账号列表")
        elif button_name == "关闭浏览器":
            self.logger.info("正在关闭浏览器...")

    def _on_clear_logs(self):
        """清空日志"""
        self.logger.info("日志已清空")

    def _on_open_log_file(self):
        """打开日志文件"""
        self.logger.info("请求打开日志文件")


class AccountPage(QWidget):
    """账号管理页面"""

    def __init__(self, logger: Logger, parent=None):
        super().__init__(parent)
        self.logger = logger

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title = QLabel("账号管理")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # 内容
        content = QLabel("这里是账号管理页面，正在开发中...")
        content.setAlignment(Qt.AlignCenter)
        layout.addWidget(content)

        # 占位空间
        layout.addStretch(1)

        self.logger.info("账号管理页面已加载")


class SettingsPage(QWidget):
    """设置页面"""

    def __init__(self, logger: Logger, parent=None):
        super().__init__(parent)
        self.logger = logger

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title = QLabel("设置")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # 内容
        content = QLabel("这里是设置页面，正在开发中...")
        content.setAlignment(Qt.AlignCenter)
        layout.addWidget(content)

        # 占位空间
        layout.addStretch(1)

        self.logger.info("设置页面已加载")


class AboutPage(QWidget):
    """关于页面"""

    def __init__(self, logger: Logger, parent=None):
        super().__init__(parent)
        self.logger = logger

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # 标题
        title = QLabel("关于")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # 内容
        content = QLabel("CursorProMax 是一个基于PySide6的界面模拟实现\n仅用于学习和研究，请勿用于商业用途")
        content.setAlignment(Qt.AlignCenter)
        content.setStyleSheet("font-size: 14px;")
        layout.addWidget(content)

        # 版本信息
        version = QLabel("版本：0.48.7")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)

        # 占位空间
        layout.addStretch(1)

        self.logger.info("关于页面已加载")


class ContentManager(QStackedWidget):
    """内容管理器"""

    def __init__(self, logger: Logger, parent=None):
        super().__init__(parent)
        self.logger = logger

        # 创建页面
        self.home_page = HomePage(logger)
        self.account_page = AccountPage(logger)
        self.settings_page = SettingsPage(logger)
        self.about_page = AboutPage(logger)

        # 添加页面
        self.addWidget(self.home_page)
        self.addWidget(self.account_page)
        self.addWidget(self.settings_page)
        self.addWidget(self.about_page)

    @Slot(str)
    def set_current_page(self, page_name):
        """设置当前页面"""
        if page_name == "home":
            self.setCurrentWidget(self.home_page)
            self.logger.info("切换到主页")
        elif page_name == "account":
            self.setCurrentWidget(self.account_page)
            self.logger.info("切换到账号管理页")
        elif page_name == "settings":
            self.setCurrentWidget(self.settings_page)
            self.logger.info("切换到设置页")
        elif page_name == "about":
            self.setCurrentWidget(self.about_page)
            self.logger.info("切换到关于页")