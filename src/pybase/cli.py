#!/usr/bin/env python3
"""
CLI 模块示例
使用 click 创建命令行界面，使用 rich 美化输出
"""

import click
from rich.console import Console
from rich.table import Table
from rich.progress import track
import time

console = Console()

@click.group()
def cli():
    """PyBase CLI 工具"""
    pass

@cli.command()
@click.option('--name', default='世界', help='要问候的名字')
def hello(name):
    """问候命令"""
    console.print(f"[bold green]你好，{name}！[/bold green]")
    console.print("欢迎使用 PyBase CLI 工具！", style="blue")

@cli.command()
@click.option('--count', default=5, help='显示的项目数量')
def list(count):
    """列出项目信息"""
    table = Table(title="项目信息")
    table.add_column("项目", style="cyan", no_wrap=True)
    table.add_column("描述", style="magenta")
    table.add_column("状态", style="green")
    
    table.add_row("PyBase", "基础 Python 包", "✅ 活跃")
    table.add_row("CLI 工具", "命令行界面", "✅ 可用")
    table.add_row("Rich 输出", "美化终端输出", "✅ 集成")
    
    console.print(table)

@cli.command()
def progress():
    """显示进度条示例"""
    console.print("[bold yellow]开始处理...[/bold yellow]")
    
    for step in track(range(100), description="处理中..."):
        time.sleep(0.01)
    
    console.print("[bold green]处理完成！[/bold green]")

if __name__ == '__main__':
    cli() 