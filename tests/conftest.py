"""
pytest 配置文件

提供测试配置和共享的 fixture
"""

import pytest
import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture(scope="session")
def test_session():
    """测试会话级别的 fixture"""
    print("\n=== 开始测试会话 ===")
    yield
    print("\n=== 测试会话结束 ===")


@pytest.fixture(scope="function")
def test_function():
    """测试函数级别的 fixture"""
    print("\n--- 开始测试函数 ---")
    yield
    print("\n--- 测试函数结束 ---")


@pytest.fixture(scope="class")
def test_class():
    """测试类级别的 fixture"""
    print("\n*** 开始测试类 ***")
    yield
    print("\n*** 测试类结束 ***")


# 自定义标记的文档
def pytest_configure(config):
    """配置 pytest"""
    # 添加自定义标记的文档
    config.addinivalue_line(
        "markers", "slow: 标记为慢速测试，可以使用 -m 'not slow' 跳过"
    )
    config.addinivalue_line(
        "markers", "integration: 标记为集成测试"
    )
    config.addinivalue_line(
        "markers", "unit: 标记为单元测试"
    )
    config.addinivalue_line(
        "markers", "cli: 标记为 CLI 相关测试"
    )
    config.addinivalue_line(
        "markers", "gui: 标记为 GUI 相关测试"
    )


# 测试收集钩子
def pytest_collection_modifyitems(config, items):
    """修改测试收集项"""
    # 为没有标记的测试添加 unit 标记
    for item in items:
        if not any(item.iter_markers()):
            item.add_marker(pytest.mark.unit)


# 测试报告钩子
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


# 测试结果钩子
def pytest_runtest_logreport(report):
    """测试运行日志报告"""
    if report.when == "call":
        if report.failed:
            print(f"❌ 测试失败: {report.nodeid}")
        elif report.passed:
            print(f"✅ 测试通过: {report.nodeid}")
        elif report.skipped:
            print(f"⏭️ 测试跳过: {report.nodeid}")


# 测试会话钩子
def pytest_sessionstart(session):
    """测试会话开始"""
    print(f"\n🚀 开始测试会话: {session.name}")
    print(f"📁 测试目录: {session.config.rootdir}")
    print(f"🐍 Python 版本: {sys.version}")


def pytest_sessionfinish(session, exitstatus):
    """测试会话结束"""
    print(f"\n测试会话结束: {session.name}")
    print(f"退出状态: {exitstatus}")
    
    # 显示测试统计
    stats = session.testscollected
    print(f"收集的测试数量: {stats}") 