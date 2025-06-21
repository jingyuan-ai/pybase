"""
CLI 功能测试
"""

import pytest
from .common import (
    cli_test, unit_test, integration_test,
    assert_cli_success, assert_cli_output_contains
)


@cli_test
def test_cli_help(cli_helper):
    """测试 CLI 帮助命令"""
    from pybase.cli import cli
    
    result = cli_helper.run_cli_command(cli, ["--help"])
    assert_cli_success(result)
    assert_cli_output_contains(result, "PyBase CLI 工具")


@cli_test
def test_cli_hello_default(cli_helper):
    """测试默认问候命令"""
    from pybase.cli import cli
    
    result = cli_helper.run_cli_command(cli, ["hello"])
    assert_cli_success(result)
    assert_cli_output_contains(result, "你好，世界")


@cli_test
def test_cli_hello_with_name(cli_helper):
    """测试带名字的问候命令"""
    from pybase.cli import cli
    
    result = cli_helper.run_cli_command(cli, ["hello", "--name", "张三"])
    assert_cli_success(result)
    assert_cli_output_contains(result, "你好，张三")


@cli_test
def test_cli_list_default(cli_helper):
    """测试默认列表命令"""
    from pybase.cli import cli
    
    result = cli_helper.run_cli_command(cli, ["list"])
    assert_cli_success(result)
    assert_cli_output_contains(result, "项目信息")


@cli_test
def test_cli_list_with_count(cli_helper):
    """测试带数量的列表命令"""
    from pybase.cli import cli
    
    result = cli_helper.run_cli_command(cli, ["list", "--count", "10"])
    assert_cli_success(result)
    assert_cli_output_contains(result, "项目信息")


@cli_test
def test_cli_progress(cli_helper):
    """测试进度命令"""
    from pybase.cli import cli
    
    result = cli_helper.run_cli_command(cli, ["progress"])
    assert_cli_success(result)
    assert_cli_output_contains(result, "处理完成")


@unit_test
def test_cli_command_structure():
    """测试 CLI 命令结构"""
    from pybase.cli import cli
    
    # 验证命令组存在
    assert hasattr(cli, 'commands')
    assert 'hello' in cli.commands
    assert 'list' in cli.commands
    assert 'progress' in cli.commands


@integration_test
def test_cli_full_workflow(cli_helper):
    """测试 CLI 完整工作流程"""
    from pybase.cli import cli
    
    # 测试所有命令
    commands = [
        ["hello"],
        ["hello", "--name", "测试用户"],
        ["list"],
        ["list", "--count", "5"],
        ["progress"]
    ]
    
    for cmd in commands:
        result = cli_helper.run_cli_command(cli, cmd)
        assert_cli_success(result) 