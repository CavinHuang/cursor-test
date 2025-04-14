# CursorProMax界面实现

基于PySide6的CursorProMax界面实现，使用模块化架构设计。

## 功能特点

- 模块化架构，清晰的代码组织
- 基于PySide6实现的现代界面
- 实现了主页、账号管理、设置和关于页面
- 集成了日志系统，支持GUI实时显示、文件记录和控制台输出

## 界面预览

界面包含以下主要部分：
- 左侧导航栏
- 主页信息显示区
- 操作按钮区
- 日志输出区

## 环境要求

- Python 3.8 或更高版本
- PySide6 6.0.0 或更高版本

## 安装与运行

1. 克隆项目到本地

2. 创建并激活虚拟环境：
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

3. 安装依赖：
```bash
uv pip install -e .
```

4. 运行应用：
```bash
python cursor_pro_max.py
```

## 项目结构

```
├── cursor_pro_max.py  # 程序入口点
├── README.md          # 项目说明文档
├── logs/              # 日志文件目录
├── pyproject.toml     # 项目依赖和配置
└── src/               # 源代码目录
    ├── __init__.py    # 包初始化文件
    ├── logger.py      # 日志管理模块
    ├── log_widget.py  # 日志显示组件
    ├── main_app.py    # 应用程序入口模块
    ├── main_frame.py  # 主框架实现
    ├── content/       # 内容页面模块
    │   ├── __init__.py
    │   └── content_pages.py
    └── navigation/    # 导航模块
        ├── __init__.py
        └── navigation.py
```

## 模块说明

1. **主框架模块**
   - `main_frame.py`: 实现应用程序主窗口框架
   - `main_app.py`: 应用程序入口，组装各模块

2. **导航模块**
   - `navigation.py`: 实现侧边栏导航功能

3. **内容页面模块**
   - `content_pages.py`: 实现各个页面的内容

4. **日志模块**
   - `logger.py`: 日志管理实现
   - `log_widget.py`: 日志显示组件

## 开发扩展

1. 添加新页面:
   - 在`content_pages.py`中创建新的页面类
   - 在`ContentManager`类中添加页面实例
   - 在`navigation.py`中添加对应的导航项
