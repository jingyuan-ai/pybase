# C++ Transform 模块构建指南

本文档介绍如何构建和安装 PyBase 的 C++ Transform 模块。

## 概述

PyBase 的 Transform 模块使用 pybind11 将 C++ 代码绑定到 Python，提供高性能的数组变换功能。

## 系统要求

### 必需依赖

- Python 3.8+
- C++ 编译器（支持 C++17）
- pybind11 >= 2.10.0
- numpy >= 1.20.0

### 推荐的 C++ 编译器

- **Linux/macOS**: GCC 7+, Clang 6+
- **Windows**: Visual Studio 2019+, MSVC 19.20+

## 安装方法

### 方法 1: 使用 pip 安装（推荐）

```bash
# 安装包含 C++ 扩展的完整版本
pip install -e .[cpp]

# 或者安装所有可选依赖
pip install -e .[cpp,cli,gui,test]
```

### 方法 2: 使用 setup.py 构建

```bash
# 安装构建依赖
pip install pybind11 numpy

# 构建和安装
python setup.py build_ext --inplace
pip install -e .
```

### 方法 3: 使用 pyproject.toml（现代方式）

```bash
# 使用 pip 构建
pip install --use-pep517 -e .

# 或使用 build
pip install build
python -m build
```

## 构建过程详解

### 1. 文件结构

```
src/pybase/
├── transform.h          # C++ 头文件
├── transform.cpp        # C++ 实现文件
├── transform_binding.cpp # pybind11 绑定文件
└── transform.py         # Python 包装模块
```

### 2. 构建配置

`setup.py` 中的关键配置：

```python
ext_modules = [
    Pybind11Extension(
        "pybase._transform",
        ["src/pybase/transform_binding.cpp", "src/pybase/transform.cpp"],
        include_dirs=[np.get_include()],
        language='c++',
        cxx_std=17,  # 使用 C++17 标准
    ),
]
```

### 3. 编译选项

可以通过环境变量自定义编译选项：

```bash
# 设置 C++ 编译器
export CXX=g++-9

# 设置编译标志
export CFLAGS="-O3 -march=native"
export CXXFLAGS="-O3 -march=native"

# 设置链接标志
export LDFLAGS="-L/usr/local/lib"
```

## 验证安装

### 1. 检查 C++ 模块是否可用

```python
from pybase.transform import get_cpp_availability
print(f"C++ 实现可用: {get_cpp_availability()}")
```

### 2. 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 只运行 C++ 相关测试
pytest tests/ -m cpp -v

# 运行 transform 测试
pytest tests/test_transform.py -v
```

### 3. 运行示例

```bash
# 运行 transform 示例
python examples/transform_example.py
```

## 故障排除

### 常见问题

#### 1. 编译错误

**问题**: `fatal error: 'pybind11/pybind11.h' file not found`

**解决方案**:
```bash
# 确保安装了 pybind11
pip install pybind11

# 或者指定 pybind11 路径
export PYBIND11_INCLUDE_DIR=/path/to/pybind11/include
```

#### 2. numpy 头文件找不到

**问题**: `fatal error: 'numpy/arrayobject.h' file not found`

**解决方案**:
```bash
# 确保安装了 numpy
pip install numpy

# 或者指定 numpy 路径
export NUMPY_INCLUDE_DIR=/path/to/numpy/include
```

#### 3. C++ 标准不支持

**问题**: `error: 'std::optional' is not a member of 'std'`

**解决方案**:
```bash
# 使用更新的编译器
export CXX=g++-9

# 或者降低 C++ 标准
# 在 setup.py 中将 cxx_std=17 改为 cxx_std=14
```

#### 4. 链接错误

**问题**: `undefined reference to 'Py_Initialize'`

**解决方案**:
```bash
# 确保链接了 Python 库
export LDFLAGS="-lpython3.8"

# 或者使用 pkg-config
export LDFLAGS=$(pkg-config --libs python3)
```

### 调试构建

#### 1. 启用详细输出

```bash
# 显示详细的编译信息
python setup.py build_ext --inplace --verbose
```

#### 2. 检查编译器版本

```bash
# 检查 C++ 编译器版本
g++ --version
clang++ --version
```

#### 3. 检查依赖版本

```python
import pybind11
import numpy
print(f"pybind11 version: {pybind11.__version__}")
print(f"numpy version: {numpy.__version__}")
```

## 性能优化

### 1. 编译优化

```bash
# 启用优化
export CXXFLAGS="-O3 -march=native -DNDEBUG"

# 启用并行编译
export MAKEFLAGS="-j$(nproc)"
```

### 2. 运行时优化

```python
# 使用 numpy 的优化
import numpy as np
np.set_printoptions(precision=6)

# 预分配数组
result = np.empty_like(input_array)
```

## 跨平台构建

### Linux

```bash
# Ubuntu/Debian
sudo apt-get install build-essential python3-dev

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
sudo yum install python3-devel
```

### macOS

```bash
# 使用 Homebrew
brew install gcc

# 设置编译器
export CC=gcc-9
export CXX=g++-9
```

### Windows

```bash
# 使用 Visual Studio
# 确保安装了 C++ 开发工具

# 或使用 MinGW
conda install m2w64-gcc
```

## 开发环境设置

### 1. 开发依赖

```bash
# 安装开发依赖
pip install -e .[cpp,test]

# 安装额外的开发工具
pip install black flake8 mypy
```

### 2. IDE 配置

#### VS Code

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.analysis.extraPaths": ["./src"],
    "C_Cpp.default.compilerPath": "/usr/bin/g++"
}
```

#### PyCharm

- 设置项目解释器为虚拟环境
- 添加 `src` 目录到 Python 路径
- 配置 C++ 工具链

### 3. 代码格式化

```bash
# 格式化 Python 代码
black src/pybase/ tests/ examples/

# 格式化 C++ 代码
clang-format -i src/pybase/*.cpp src/pybase/*.h
```

## 发布构建

### 1. 构建轮子

```bash
# 构建源码分发
python setup.py sdist

# 构建轮子
python setup.py bdist_wheel

# 或使用 build
python -m build --wheel
```

### 2. 多平台构建

```bash
# 使用 cibuildwheel（CI/CD）
cibuildwheel --platform linux --python 3.8 3.9 3.10 3.11 3.12

# 或使用 docker
docker run --rm -v $PWD:/io quay.io/pypa/manylinux2014_x86_64 /io/build-wheels.sh
```

## 总结

通过以上步骤，你可以成功构建和安装 PyBase 的 C++ Transform 模块。如果遇到问题，请参考故障排除部分或查看项目文档。 