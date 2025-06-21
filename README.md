# PyBase

一个基础的 Python 包，支持命令行界面（CLI）和图形用户界面（GUI）。

## 功能特性

- 🐍 基础 Python 包结构
- 🖥️ 命令行界面（CLI）支持
- 🖼️ 图形用户界面（GUI）支持
- 📦 可选依赖管理
- 🧪 完整的测试框架
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

### 安装测试功能
```bash
pip install .[test]
```

### 安装所有功能
```bash
pip install .[cli,gui,test]
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

## 测试

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定类型的测试
pytest -m unit      # 单元测试
pytest -m cli       # CLI 测试
pytest -m gui       # GUI 测试
pytest -m integration  # 集成测试

# 生成覆盖率报告
pytest --cov=src/pybase --cov-report=html:htmlcov
```

### 测试特性
- **pytest 插件**: 自定义测试工具和标记
- **测试数据管理**: 自动清理临时文件和目录
- **CLI 测试**: 完整的命令行测试支持
- **GUI 测试**: 模拟和真实环境测试
- **覆盖率报告**: HTML 和终端覆盖率显示

详细测试说明请参考 [测试指南](docs/TESTING.md)

## 项目结构

```
pybase/
├── src/
│   └── pybase/
│       ├── __init__.py
│       ├── utils.py
│       ├── cli.py          # CLI 功能
│       ├── gui.py          # GUI 功能
│       └── testing.py      # pytest 插件
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # pytest 配置
│   ├── test_utils.py       # 工具函数测试
│   ├── test_cli.py         # CLI 功能测试
│   ├── test_gui.py         # GUI 功能测试
│   └── test_simple.py      # 简单测试
├── docs/
│   └── TESTING.md          # 测试详细说明
├── pyproject.toml          # 项目配置
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

### 测试可选依赖
- `pytest` - 测试框架
- `pytest-cov` - 覆盖率测试
- `pytest-mock` - 模拟测试
- `pytest-html` - HTML 测试报告

## 开发

### 本地开发安装
```bash
# 安装开发版本
pip install -e .

# 安装所有可选依赖
pip install -e .[cli,gui,test]
```

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_utils.py

# 生成覆盖率报告
pytest --cov=src/pybase --cov-report=html:htmlcov
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

#### 添加新的测试
在 `tests/` 目录中创建测试文件：

```python
from .common import unit_test

@unit_test
def test_new_function():
    """测试新功能"""
    assert new_function() == expected_result
```

## 优势

1. **模块化设计** - 基础功能、CLI、GUI、测试分离
2. **可选依赖** - 用户按需安装功能
3. **跨平台** - 支持 Windows、macOS、Linux
4. **完整测试** - 包含单元测试、集成测试、覆盖率报告
5. **易于扩展** - 清晰的代码结构和文档
6. **用户友好** - 直观的界面和操作

## 详细文档

- [测试指南](docs/TESTING.md) - 完整的测试使用说明

## 许可证

MIT License

## 作者

damon <damon@china.com>