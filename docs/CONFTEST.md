# conftest.py 详解

## 概述

`conftest.py` 是 pytest 的特殊配置文件，用于定义测试配置、共享 fixtures 和钩子函数。pytest 会自动发现和加载这个文件，无需手动导入。

## 作用机制

### 1. 自动发现
- pytest 从当前目录开始向上搜索 `conftest.py` 文件
- 自动加载找到的配置文件
- 配置应用到该目录及其子目录的所有测试

### 2. 作用域
```
pybase/
├── conftest.py          # 项目根目录配置（可选）
├── tests/
│   ├── conftest.py      # 测试目录配置
│   ├── test_utils.py
│   └── test_cli.py
└── src/
    └── pybase/
```

- 子目录继承父目录的配置
- 可以覆盖父目录的配置
- 同级目录的配置相互独立

## 我们的 conftest.py 分析

### 1. 路径配置
```python
# 添加 src 目录到 Python 路径
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))
```

**作用：**
- 让测试能够导入 `src/pybase` 模块
- 解决模块导入路径问题
- 支持开发模式下的测试

### 2. Fixtures 定义

#### 会话级别 Fixture
```python
@pytest.fixture(scope="session")
def test_session():
    """测试会话级别的 fixture"""
    print("\n=== 开始测试会话 ===")
    yield
    print("\n=== 测试会话结束 ===")
```

**特点：**
- 整个测试会话期间只创建一次
- 所有测试共享同一个实例
- 适合设置和清理全局资源

#### 函数级别 Fixture
```python
@pytest.fixture(scope="function")
def test_function():
    """测试函数级别的 fixture"""
    print("\n--- 开始测试函数 ---")
    yield
    print("\n--- 测试函数结束 ---")
```

**特点：**
- 每个测试函数执行时创建
- 测试结束后自动清理
- 适合每个测试的独立设置

#### 类级别 Fixture
```python
@pytest.fixture(scope="class")
def test_class():
    """测试类级别的 fixture"""
    print("\n*** 开始测试类 ***")
    yield
    print("\n*** 测试类结束 ***")
```

**特点：**
- 每个测试类执行时创建
- 类内所有测试共享
- 适合类级别的设置

### 3. 钩子函数

#### pytest_configure
```python
def pytest_configure(config):
    """配置 pytest"""
    # 添加自定义标记的文档
    config.addinivalue_line("markers", "slow: 标记为慢速测试")
    config.addinivalue_line("markers", "integration: 标记为集成测试")
    # ... 更多标记
```

**调用时机：** pytest 启动时，配置阶段
**作用：** 注册自定义标记、配置选项

#### pytest_collection_modifyitems
```python
def pytest_collection_modifyitems(config, items):
    """修改测试收集项"""
    # 为没有标记的测试添加 unit 标记
    for item in items:
        if not any(item.iter_markers()):
            item.add_marker(pytest.mark.unit)
```

**调用时机：** 测试收集完成后，运行前
**作用：** 修改测试项、添加标记、过滤测试

#### pytest_sessionstart/finish
```python
def pytest_sessionstart(session):
    """测试会话开始"""
    print(f"\n🚀 开始测试会话: {session.name}")
    print(f"📁 测试目录: {session.config.rootdir}")
    print(f"🐍 Python 版本: {sys.version}")

def pytest_sessionfinish(session, exitstatus):
    """测试会话结束"""
    print(f"\n🏁 测试会话结束: {session.name}")
    print(f"📊 退出状态: {exitstatus}")
    stats = session.testscollected
    print(f"📈 收集的测试数量: {stats}")
```

**调用时机：** 会话开始/结束时
**作用：** 初始化、清理、生成报告

#### pytest_runtest_logreport
```python
def pytest_runtest_logreport(report):
    """测试运行日志报告"""
    if report.when == "call":
        if report.failed:
            print(f"❌ 测试失败: {report.nodeid}")
        elif report.passed:
            print(f"✅ 测试通过: {report.nodeid}")
        elif report.skipped:
            print(f"⏭️ 测试跳过: {report.nodeid}")
```

**调用时机：** 每个测试运行后
**作用：** 处理测试结果、自定义输出

#### HTML 报告钩子
```python
def pytest_html_report_title(report):
    """自定义 HTML 报告标题"""
    report.title = "PyBase 测试报告"

def pytest_html_results_summary(prefix, summary, postfix):
    """自定义 HTML 报告摘要"""
    prefix.extend([
        "<h2>测试环境</h2>",
        "<p>Python 版本: " + sys.version + "</p>",
        "<p>测试框架: pytest</p>",
    ])
```

**调用时机：** 生成 HTML 报告时
**作用：** 自定义报告内容和格式

## 调用流程

### 完整的测试执行流程

```bash
pytest tests/test_utils.py -v
```

**执行步骤：**

1. **pytest 启动**
   - 扫描当前目录及父目录的 `conftest.py`
   - 加载配置文件

2. **pytest_sessionstart()**
   - 打印会话开始信息
   - 显示 Python 版本和测试目录

3. **pytest_configure()**
   - 注册自定义标记
   - 配置测试选项

4. **收集测试文件**
   - 扫描指定的测试文件
   - 识别测试函数和类

5. **pytest_collection_modifyitems()**
   - 为没有标记的测试添加 `unit` 标记
   - 修改测试项列表

6. **运行测试**
   - 为每个测试创建 fixtures
   - 执行测试函数

7. **pytest_runtest_logreport()**
   - 处理每个测试的结果
   - 打印通过/失败/跳过信息

8. **pytest_sessionfinish()**
   - 打印会话结束信息
   - 显示测试统计

## 使用示例

### 1. 在测试中使用 Fixtures

```python
def test_with_fixtures(test_session, test_function):
    """使用 conftest.py 中定义的 fixtures"""
    # test_session 在整个会话期间有效
    # test_function 在每个测试函数执行时调用
    assert True
```

### 2. 自动标记应用

```python
def test_simple():
    """没有显式标记的测试"""
    assert True
    # 自动添加 @pytest.mark.unit 标记
```

### 3. 自定义输出

运行测试时会看到：
```
🚀 开始测试会话: pybase
📁 测试目录: /path/to/pybase
🐍 Python 版本: 3.12.9

--- 开始测试函数 ---
✅ 测试通过: tests/test_utils.py::test_simple
--- 测试函数结束 ---

🏁 测试会话结束: pybase
📊 退出状态: 0
📈 收集的测试数量: 1
```

## 最佳实践

### 1. Fixture 设计
- 使用合适的 scope（session/class/function）
- 提供清晰的文档字符串
- 处理异常和清理资源

### 2. 钩子函数
- 只做必要的配置和修改
- 提供有用的日志信息
- 避免副作用

### 3. 路径配置
- 使用相对路径
- 考虑不同环境下的兼容性
- 提供清晰的错误信息

### 4. 标记管理
- 定义有意义的标记名称
- 提供标记的文档说明
- 避免标记冲突

## 调试技巧

### 1. 检查 conftest.py 是否被加载
```python
# 在 conftest.py 中添加
print("conftest.py 被加载了！")
```

### 2. 调试 Fixtures
```python
@pytest.fixture(scope="function")
def debug_fixture():
    print("Fixture 被调用了")
    yield "fixture_value"
    print("Fixture 清理了")
```

### 3. 调试钩子函数
```python
def pytest_configure(config):
    print("pytest_configure 被调用了")
    # ... 其他代码
```

### 4. 检查路径配置
```python
import sys
print("Python 路径:", sys.path)
```

## 常见问题

### 1. conftest.py 没有被加载
**原因：** 文件位置不正确或命名错误
**解决：** 确保文件名为 `conftest.py` 且在正确的目录

### 2. Fixtures 不可用
**原因：** scope 设置不正确或导入问题
**解决：** 检查 fixture 定义和导入

### 3. 路径配置不工作
**原因：** 路径计算错误或权限问题
**解决：** 使用绝对路径或检查文件权限

### 4. 钩子函数没有被调用
**原因：** 函数名错误或参数不匹配
**解决：** 检查函数签名和 pytest 文档

## 总结

`conftest.py` 是 pytest 测试框架的核心配置文件：

1. **自动发现和加载** - pytest 自动处理
2. **共享配置** - 为整个测试目录提供配置
3. **Fixtures 定义** - 提供测试数据和环境
4. **钩子函数** - 自定义测试行为
5. **路径管理** - 解决模块导入问题

通过合理使用 `conftest.py`，可以：
- 减少重复代码
- 统一测试配置
- 提供更好的测试体验
- 简化测试维护 