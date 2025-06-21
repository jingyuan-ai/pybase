"""
PyBase pytest 插件

提供测试工具、自定义标记和测试辅助功能
"""

import pytest
import os
import tempfile
import shutil
from pathlib import Path
from typing import Generator, Any, Dict, List


def pytest_configure(config):
    """配置 pytest"""
    # 注册自定义标记
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "cli: marks tests as CLI related"
    )
    config.addinivalue_line(
        "markers", "gui: marks tests as GUI related"
    )


def pytest_collection_modifyitems(config, items):
    """修改测试收集项"""
    # 为没有标记的测试添加 unit 标记
    for item in items:
        if not any(item.iter_markers()):
            item.add_marker(pytest.mark.unit)


class TestData:
    """测试数据管理类"""
    
    def __init__(self):
        self._temp_dirs = []
        self._temp_files = []
    
    def create_temp_dir(self) -> Path:
        """创建临时目录"""
        temp_dir = Path(tempfile.mkdtemp(prefix="pybase_test_"))
        self._temp_dirs.append(temp_dir)
        return temp_dir
    
    def create_temp_file(self, content: str = "", suffix: str = ".txt") -> Path:
        """创建临时文件"""
        temp_file = Path(tempfile.mktemp(suffix=suffix, prefix="pybase_test_"))
        if content:
            temp_file.write_text(content, encoding='utf-8')
        self._temp_files.append(temp_file)
        return temp_file
    
    def cleanup(self):
        """清理临时文件和目录"""
        for temp_file in self._temp_files:
            if temp_file.exists():
                temp_file.unlink()
        
        for temp_dir in self._temp_dirs:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)


@pytest.fixture(scope="function")
def test_data() -> Generator[TestData, None, None]:
    """提供测试数据管理"""
    data = TestData()
    yield data
    data.cleanup()


@pytest.fixture(scope="function")
def temp_dir(test_data) -> Path:
    """提供临时目录"""
    return test_data.create_temp_dir()


@pytest.fixture(scope="function")
def temp_file(test_data) -> Path:
    """提供临时文件"""
    return test_data.create_temp_file()


@pytest.fixture(scope="function")
def sample_text_file(test_data) -> Path:
    """提供示例文本文件"""
    content = """这是示例文本文件
包含多行内容
用于测试文件操作功能
"""
    return test_data.create_temp_file(content, ".txt")


@pytest.fixture(scope="function")
def mock_env(monkeypatch):
    """提供环境变量模拟"""
    def _set_env(**kwargs):
        for key, value in kwargs.items():
            monkeypatch.setenv(key, str(value))
    return _set_env


@pytest.fixture(scope="function")
def mock_stdin(monkeypatch):
    """模拟标准输入"""
    def _mock_input(input_text: str):
        monkeypatch.setattr('builtins.input', lambda: input_text)
    return _mock_input


@pytest.fixture(scope="function")
def capture_output(capsys):
    """捕获输出"""
    def _capture():
        captured = capsys.readouterr()
        return captured.out, captured.err
    return _capture


class CLIHelper:
    """CLI 测试辅助类"""
    
    @staticmethod
    def run_cli_command(cli_func, args: List[str], **kwargs) -> Any:
        """运行 CLI 命令"""
        import click
        from click.testing import CliRunner
        
        runner = CliRunner()
        result = runner.invoke(cli_func, args, **kwargs)
        return result


@pytest.fixture(scope="function")
def cli_helper() -> CLIHelper:
    """提供 CLI 测试辅助"""
    return CLIHelper()


class GUIHelper:
    """GUI 测试辅助类"""
    
    @staticmethod
    def skip_if_no_gui():
        """如果没有 GUI 支持则跳过测试"""
        try:
            import PyQt5
        except ImportError:
            pytest.skip("PyQt5 not available")
    
    @staticmethod
    def create_test_app():
        """创建测试应用"""
        from PyQt5.QtWidgets import QApplication
        import sys
        
        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()
        return app


@pytest.fixture(scope="function")
def gui_helper() -> GUIHelper:
    """提供 GUI 测试辅助"""
    return GUIHelper()


@pytest.fixture(scope="function")
def mock_gui_dependencies(monkeypatch):
    """模拟 GUI 依赖"""
    # 模拟 PyQt5 模块
    class MockQApplication:
        def __init__(self, *args, **kwargs):
            pass
        
        def exec_(self):
            return 0
    
    class MockQMainWindow:
        def __init__(self):
            pass
        
        def show(self):
            pass
    
    monkeypatch.setattr("PyQt5.QtWidgets.QApplication", MockQApplication)
    monkeypatch.setattr("PyQt5.QtWidgets.QMainWindow", MockQMainWindow)


# 自定义断言函数
def assert_file_exists(file_path: Path):
    """断言文件存在"""
    assert file_path.exists(), f"文件不存在: {file_path}"


def assert_file_content(file_path: Path, expected_content: str):
    """断言文件内容"""
    assert file_path.exists(), f"文件不存在: {file_path}"
    actual_content = file_path.read_text(encoding='utf-8')
    assert actual_content == expected_content, f"文件内容不匹配"


def assert_dir_exists(dir_path: Path):
    """断言目录存在"""
    assert dir_path.exists(), f"目录不存在: {dir_path}"
    assert dir_path.is_dir(), f"路径不是目录: {dir_path}"


def assert_cli_success(result):
    """断言 CLI 命令执行成功"""
    assert result.exit_code == 0, f"CLI 命令失败: {result.output}"


def assert_cli_output_contains(result, text: str):
    """断言 CLI 输出包含指定文本"""
    assert text in result.output, f"输出中不包含 '{text}': {result.output}"


# 测试装饰器
def slow_test(func):
    """标记为慢速测试"""
    return pytest.mark.slow(func)


def integration_test(func):
    """标记为集成测试"""
    return pytest.mark.integration(func)


def unit_test(func):
    """标记为单元测试"""
    return pytest.mark.unit(func)

def cpp_test(func):
    """标记为 C++ 测试"""
    return pytest.mark.cpp(func)

def cli_test(func):
    """标记为 CLI 测试"""
    return pytest.mark.cli(func)


def gui_test(func):
    """标记为 GUI 测试"""
    return pytest.mark.gui(func)


# 测试数据生成器
class TestDataGenerator:
    """测试数据生成器"""
    
    @staticmethod
    def generate_random_text(length: int = 100) -> str:
        """生成随机文本"""
        import random
        import string
        
        chars = string.ascii_letters + string.digits + " \n\t"
        return ''.join(random.choice(chars) for _ in range(length))
    
    @staticmethod
    def generate_test_numbers(count: int = 10) -> List[float]:
        """生成测试数字"""
        import random
        
        return [random.uniform(-100, 100) for _ in range(count)]
    
    @staticmethod
    def generate_test_strings(count: int = 5) -> List[str]:
        """生成测试字符串"""
        return [f"test_string_{i}" for i in range(count)]


@pytest.fixture(scope="function")
def data_generator() -> TestDataGenerator:
    """提供测试数据生成器"""
    return TestDataGenerator()