# PyBase CLI 使用指南

## 安装

### 1. 安装基础包（不包含 CLI 功能）
```bash
pip install .
```

### 2. 安装包含 CLI 功能的完整包
```bash
pip install .[cli]
```

## 使用方法

安装完成后，你可以使用以下命令：

### 基本命令
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

### 命令详解

#### `hello` 命令
- **功能**: 显示问候信息
- **选项**: 
  - `--name`: 指定要问候的名字（默认：世界）

#### `list` 命令
- **功能**: 以表格形式显示项目信息
- **选项**:
  - `--count`: 显示的项目数量（默认：5）

#### `progress` 命令
- **功能**: 演示进度条功能

## 开发说明

### 依赖包说明
- **click**: 用于创建命令行界面
- **rich**: 用于美化终端输出（表格、进度条、颜色等）

### 添加新命令
在 `src/pybase/cli.py` 中添加新的命令：

```python
@cli.command()
@click.option('--option', default='value', help='选项说明')
def new_command(option):
    """新命令的描述"""
    console.print(f"新命令执行，选项：{option}")
```

### 运行开发版本
```bash
# 在项目根目录运行
python src/pybase/cli.py hello
```

## 优势

1. **可选依赖**: 用户可以选择是否安装 CLI 功能
2. **美化输出**: 使用 rich 提供彩色输出和表格显示
3. **易于扩展**: 使用 click 框架，添加新命令很简单
4. **用户友好**: 自动生成帮助文档和参数验证 