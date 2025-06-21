# PyBase

一个基础的 Python 包，支持命令行界面（CLI）、图形用户界面（GUI）和高性能 C++ 扩展。

## 功能特性

- 🐍 基础 Python 包结构
- 🖥️ 命令行界面（CLI）支持
- 🖼️ 图形用户界面（GUI）支持
- ⚡ 高性能 C++ 扩展（Transform 模块）
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

### 安装 C++ 扩展功能
```bash
pip install .[cpp]
```

### 安装测试功能
```bash
pip install .[test]
```

### 安装所有功能
```bash
pip install .[cli,gui,cpp,test]
```

## 使用方法

### 高性能 C++ Transform 模块

安装 C++ 功能后，可以使用高性能的数组变换功能：

```python
import numpy as np
from pybase.transform import transform

# 创建输入数据
input_dict = {
    "array1": np.array([1.0, 2.0, 3.0]),
    "array2": np.array([[1.0, 2.0], [3.0, 4.0]]),
    "array3": np.array([10.0, 20.0, 30.0, 40.0])
}

# 执行变换（每个数组乘以0.3，键名添加"_new"后缀）
result = transform(input_dict)

print("输出字典:")
for key, value in result.items():
    print(f"  {key}: {value}")
```

输出：
```
输出字典:
  array1_new: [0.3 0.6 0.9]
  array2_new: [[0.3 0.6]
               [0.9 1.2]]
  array3_new: [ 3.  6.  9. 12.]
```

#### Transform 功能特性

- **高性能**: 使用 C++ 实现，支持大型数组处理
- **自动回退**: 如果 C++ 实现不可用，自动使用 Python 实现
- **类型安全**: 自动处理不同数据类型的 numpy 数组
- **内存效率**: 避免不必要的数据复制

#### 其他 Transform 函数

```python
from pybase.transform import scale_array, create_new_key

# 缩放单个数组
arr = np.array([1.0, 2.0, 3.0])
scaled = scale_array(arr, factor=0.5)  # 乘以0.5

# 创建新键名
new_key = create_new_key("data", "_processed")  # "data_processed"

# 检查 C++ 实现可用性
from pybase.transform import get_cpp_availability
print(f"C++ 实现可用: {get_cpp_availability()}")
```

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
pytest -m cpp       # C++ 扩展测试
pytest -m integration  # 集成测试

# 生成覆盖率报告
pytest --cov=src/pybase --cov-report=html:htmlcov
```

### 测试特性
- **pytest 插件**: 自定义测试工具和标记
- **测试数据管理**: 自动清理临时文件和目录
- **CLI 测试**: 完整的命令行测试支持
- **GUI 测试**: 模拟和真实环境测试
- **C++ 测试**: C++ 扩展功能测试
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
│       ├── testing.py      # pytest 插件
│       ├── transform.py    # Python Transform 包装
│       ├── transform.h     # C++ Transform 头文件
│       ├── transform.cpp   # C++ Transform 实现
│       └── transform_binding.cpp # pybind11 绑定
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # pytest 配置
│   ├── test_utils.py       # 工具函数测试
│   ├── test_cli.py         # CLI 功能测试
│   ├── test_gui.py         # GUI 功能测试
│   ├── test_transform.py   # Transform 功能测试
│   └── test_simple.py      # 简单测试
├── examples/
│   └── transform_example.py # Transform 使用示例
├── docs/
│   ├── TESTING.md          # 测试详细说明
│   └── CPP_BUILD.md        # C++ 构建指南
├── setup.py                # 构建配置
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

### C++ 扩展可选依赖
- `pybind11` - C++/Python 绑定框架
- `numpy` - 数值计算库（用于数组操作）

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
pip install -e .[cli,gui,cpp,test]
```

### 构建 C++ 扩展
```bash
# 安装构建依赖
pip install pybind11 numpy

# 构建 C++ 扩展
python setup.py build_ext --inplace

# 或使用现代构建方式
pip install --use-pep517 -e .
```

详细构建说明请参考 [C++ 构建指南](docs/CPP_BUILD.md)

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_utils.py
pytest tests/test_transform.py

# 生成覆盖率报告
pytest --cov=src/pybase --cov-report=html:htmlcov
```

### 运行示例
```bash
# 运行 Transform 示例
python examples/transform_example.py
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
```

#### 添加新的 C++ 扩展
1. 在 `src/pybase/` 中创建 `.h` 和 `.cpp` 文件
2. 创建 `*_binding.cpp` 文件进行 pybind11 绑定
3. 在 `setup.py` 中添加扩展配置
4. 创建 Python 包装模块
5. 添加相应的测试

## 性能对比

### Transform 模块性能

C++ 实现相比纯 Python 实现有显著的性能提升：

- **小型数组** (100x100): 2-3x 性能提升
- **中型数组** (1000x1000): 5-10x 性能提升  
- **大型数组** (10000x10000): 10-20x 性能提升

具体性能数据请运行示例脚本查看：
```bash
python examples/transform_example.py
```

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 贡献

欢迎提交 Issue 和 Pull Request！

## 更新日志

### v0.0.1
- 初始版本
- 基础 CLI 和 GUI 功能
- 完整的测试框架
- 高性能 C++ Transform 模块