# PyBase

一个基础的 Python 包，支持命令行界面（CLI）和图形用户界面（GUI）。

## 功能特性

- 🐍 基础 Python 包结构
- 🖥️ 命令行界面（CLI）支持
- 🖼️ 图形用户界面（GUI）支持
- 📦 可选依赖管理
- 🔧 易于扩展和定制

## 安装

### 基础安装
```bash
pip install .
```

### 安装 CLI 功能
```bash
pip install .[cli]
```

### 安装 GUI 功能
```bash
pip install .[gui]
```

### 安装所有功能
```bash
pip install .[cli,gui]
```

## 使用方法

### 命令行界面 (CLI)

安装 CLI 功能后，可以使用以下命令：

```bash
# 查看帮助
pybase --help

# 问候命令
pybase hello
pybase hello --name 张三

# 列出项目信息
pybase list
pybase list --count 10

# 显示进度条示例
pybase progress
```

### 图形用户界面 (GUI)

安装 GUI 功能后，可以使用以下命令启动：

```bash
# 启动 GUI 应用
pybase-gui

# 或者直接运行 Python 文件
python src/pybase/gui.py
```

GUI 应用包含四个主要功能标签页：

1. **基础功能** - 用户输入、问候、主题选择
2. **计算器** - 简单的四则运算
3. **文件操作** - 文件读取、编辑、保存
4. **进度演示** - 进度条和动画演示

## 项目结构

```
pybase/
├── src/
│   └── pybase/
│       ├── __init__.py
│       ├── utils.py
│       ├── cli.py          # CLI 功能
│       └── gui.py          # GUI 功能
├── tests/
├── pyproject.toml          # 项目配置
├── docs/
├── docs/CLI_USAGE.md           # CLI 详细使用说明
├── docs/GUI_USAGE.md           # GUI 详细使用说明
└── README.md              # 项目说明
```

## 依赖说明

### 基础依赖
- `numpy` - 数值计算库

### CLI 可选依赖
- `rich` - 终端美化输出
- `click` - 命令行界面框架

### GUI 可选依赖
- `PyQt5` - 跨平台 GUI 框架

## 开发

### 本地开发安装
```bash
# 安装开发版本
pip install -e .

# 安装所有可选依赖
pip install -e .[cli,gui]
```

### 运行测试
```bash
# 测试 CLI 功能
python src/pybase/cli.py hello

# 测试 GUI 功能
python test_gui.py
```

### 添加新功能

#### 添加新的 CLI 命令
在 `src/pybase/cli.py` 中添加：

```python
@cli.command()
@click.option('--option', default='value', help='选项说明')
def new_command(option):
    """新命令的描述"""
    console.print(f"新命令执行，选项：{option}")
```

#### 添加新的 GUI 标签页
在 `src/pybase/gui.py` 中添加：

```python
def create_new_tab(self):
    """创建新标签页"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    
    # 添加你的控件
    title = QLabel("新功能")
    layout.addWidget(title)
    
    return widget

# 在 init_ui 方法中添加：
tab_widget.addTab(self.create_new_tab(), "新功能")
```

## 优势

1. **模块化设计** - 基础功能、CLI、GUI 分离
2. **可选依赖** - 用户按需安装功能
3. **跨平台** - 支持 Windows、macOS、Linux
4. **易于扩展** - 清晰的代码结构和文档
5. **用户友好** - 直观的界面和操作

## 详细文档

- [CLI 使用指南](CLI_USAGE.md) - 命令行界面的详细使用说明
- [GUI 使用指南](GUI_USAGE.md) - 图形界面的详细使用说明

## 许可证

MIT License

## 作者

damon <damon@china.com>