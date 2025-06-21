# PyBase 测试指南

## 概述

PyBase 使用 pytest 作为测试框架，并提供了丰富的测试工具和自定义插件。

## 安装测试依赖

### 安装所有测试依赖
```bash
pip install .[test]
```

### 单独安装测试包
```bash
pip install pytest pytest-cov pytest-mock pytest-html
```

## 运行测试

### 运行所有测试
```bash
pytest
```

### 运行特定测试文件
```bash
pytest tests/test_utils.py
pytest tests/test_cli.py
pytest tests/test_gui.py
```

### 运行特定测试函数
```bash
pytest tests/test_utils.py::test_data_generator_random_text
```

### 运行特定标记的测试
```bash
# 只运行单元测试
pytest -m unit

# 只运行 CLI 测试
pytest -m cli

# 只运行 GUI 测试
pytest -m gui

# 跳过慢速测试
pytest -m "not slow"

# 运行集成测试
pytest -m integration
```

## 测试标记

PyBase 定义了以下测试标记：

- `@unit_test` - 单元测试
- `@integration_test` - 集成测试
- `@slow_test` - 慢速测试
- `@cli_test` - CLI 相关测试
- `@gui_test` - GUI 相关测试

### 使用示例
```python
from pybase.testing import unit_test, integration_test

@unit_test
def test_simple_function():
    """简单的单元测试"""
    assert 1 + 1 == 2

@integration_test
def test_complex_workflow():
    """复杂的集成测试"""
    # 测试完整的工作流程
    pass
```

## 测试 Fixtures

### 基础 Fixtures

#### `test_data`
提供测试数据管理，自动清理临时文件和目录。

```python
def test_file_operations(test_data):
    # 创建临时文件
    temp_file = test_data.create_temp_file("测试内容")
    
    # 创建临时目录
    temp_dir = test_data.create_temp_dir()
    
    # 测试完成后自动清理
```

#### `temp_dir` / `temp_file`
直接提供临时目录或文件。

```python
def test_with_temp_dir(temp_dir):
    # 使用临时目录
    test_file = temp_dir / "test.txt"
    test_file.write_text("内容")
    assert test_file.exists()

def test_with_temp_file(temp_file):
    # 使用临时文件
    temp_file.write_text("内容")
    assert temp_file.read_text() == "内容"
```

#### `sample_text_file`
提供预定义的示例文本文件。

```python
def test_file_reading(sample_text_file):
    content = sample_text_file.read_text()
    assert "示例文本文件" in content
```

### CLI 测试 Fixtures

#### `cli_helper`
提供 CLI 命令测试辅助。

```python
def test_cli_command(cli_helper):
    from pybase.cli import cli
    
    result = cli_helper.run_cli_command(cli, ["hello", "--name", "张三"])
    assert result.exit_code == 0
    assert "你好，张三" in result.output
```

### GUI 测试 Fixtures

#### `gui_helper`
提供 GUI 测试辅助。

```python
def test_gui_creation(gui_helper):
    # 检查 GUI 依赖是否可用
    gui_helper.skip_if_no_gui()
    
    # 创建测试应用
    app = gui_helper.create_test_app()
    assert app is not None
```

#### `mock_gui_dependencies`
模拟 GUI 依赖，用于在没有 GUI 环境的情况下测试。

```python
def test_gui_with_mock(mock_gui_dependencies):
    from pybase.gui import PyBaseGUI
    
    # 可以创建 GUI 实例而不会出错
    gui = PyBaseGUI()
    assert gui is not None
```

## 自定义断言函数

### 文件相关断言

```python
from pybase.testing import assert_file_exists, assert_file_content, assert_dir_exists

def test_file_operations():
    # 断言文件存在
    assert_file_exists(file_path)
    
    # 断言文件内容
    assert_file_content(file_path, "期望的内容")
    
    # 断言目录存在
    assert_dir_exists(dir_path)
```

### CLI 相关断言

```python
from pybase.testing import assert_cli_success, assert_cli_output_contains

def test_cli_command():
    result = cli_helper.run_cli_command(cli, ["hello"])
    
    # 断言命令执行成功
    assert_cli_success(result)
    
    # 断言输出包含特定文本
    assert_cli_output_contains(result, "你好")
```

## 测试数据生成器

### `data_generator`
提供测试数据生成功能。

```python
def test_data_generation(data_generator):
    # 生成随机文本
    text = data_generator.generate_random_text(100)
    assert len(text) == 100
    
    # 生成测试数字
    numbers = data_generator.generate_test_numbers(5)
    assert len(numbers) == 5
    
    # 生成测试字符串
    strings = data_generator.generate_test_strings(3)
    assert len(strings) == 3
```

## 测试覆盖率

### 运行覆盖率测试
```bash
# 生成覆盖率报告
pytest --cov=src/pybase --cov-report=html:htmlcov

# 在终端显示覆盖率
pytest --cov=src/pybase --cov-report=term-missing

# 生成多种格式的报告
pytest --cov=src/pybase --cov-report=html:htmlcov --cov-report=term-missing
```

### 查看覆盖率报告
```bash
# 打开 HTML 报告
open htmlcov/index.html
```

## 测试报告

### HTML 报告
```bash
# 生成 HTML 报告
pytest --html=reports/report.html --self-contained-html
```

### JUnit XML 报告
```bash
# 生成 JUnit XML 报告
pytest --junitxml=reports/junit.xml
```

## 测试配置

### pytest.ini 配置
项目根目录的 `pyproject.toml` 中包含了完整的 pytest 配置：

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--verbose",
    "--tb=short",
    "--cov=src/pybase",
    "--cov-report=html:htmlcov",
    "--cov-report=term-missing",
]
```

### 覆盖率配置
```toml
[tool.coverage.run]
source = ["src/pybase"]
omit = [
    "*/tests/*",
    "*/test_*",
    "*/__pycache__/*",
]
```

## 最佳实践

### 1. 测试命名
- 测试文件以 `test_` 开头
- 测试函数以 `test_` 开头
- 测试类以 `Test` 开头

### 2. 测试组织
- 单元测试放在 `tests/test_*.py` 文件中
- 按功能模块组织测试文件
- 使用适当的测试标记

### 3. 测试数据
- 使用 `test_data` fixture 管理临时数据
- 避免在测试中硬编码数据
- 使用数据生成器创建测试数据

### 4. 测试隔离
- 每个测试应该是独立的
- 使用 fixture 设置和清理测试环境
- 避免测试之间的依赖

### 5. 测试覆盖
- 保持高测试覆盖率
- 重点测试核心功能
- 包含边界条件和错误情况

## 常见问题

### Q: 如何跳过某些测试？
A: 使用 `@pytest.mark.skip` 或 `@pytest.mark.skipif`

```python
@pytest.mark.skip(reason="暂时跳过")
def test_skipped():
    pass

@pytest.mark.skipif(sys.version_info < (3, 8), reason="需要 Python 3.8+")
def test_python_version():
    pass
```

### Q: 如何参数化测试？
A: 使用 `@pytest.mark.parametrize`

```python
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
    (3, 6),
])
def test_multiply_by_2(input, expected):
    assert input * 2 == expected
```

### Q: 如何模拟外部依赖？
A: 使用 `pytest-mock` 或 `unittest.mock`

```python
def test_with_mock(mocker):
    # 模拟函数
    mock_func = mocker.patch('module.function')
    mock_func.return_value = 'mocked'
    
    # 测试代码
    result = some_function()
    assert result == 'mocked'
```

## 持续集成

### GitHub Actions 示例
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        pip install .[test]
    - name: Run tests
      run: |
        pytest --cov=src/pybase --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v1
``` 