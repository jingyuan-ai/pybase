#!/usr/bin/env python3
"""
现代 C++ 扩展构建脚本

使用 pyproject.toml 和 PEP 517 标准构建 C++ 扩展
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    if version < (3, 8):
        print("❌ 错误: 需要 Python 3.8 或更高版本")
        print(f"   当前版本: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python 版本: {version.major}.{version.minor}.{version.micro}")
    return True


def check_compiler():
    """检查 C++ 编译器"""
    system = platform.system().lower()
    
    if system == "windows":
        # Windows 上检查 MSVC
        try:
            result = subprocess.run(
                ["cl"], 
                capture_output=True, 
                text=True, 
                shell=True
            )
            if result.returncode == 0 or "Microsoft" in result.stderr:
                print("✅ 找到 MSVC 编译器")
                return True
        except FileNotFoundError:
            pass
        
        print("❌ 未找到 MSVC 编译器")
        print("   请安装 Visual Studio 或 Visual Studio Build Tools")
        return False
    
    else:
        # Linux/macOS 上检查 GCC 或 Clang
        compilers = ["g++", "clang++"]
        
        for compiler in compilers:
            try:
                result = subprocess.run(
                    [compiler, "--version"], 
                    capture_output=True, 
                    text=True
                )
                if result.returncode == 0:
                    version_line = result.stdout.split('\n')[0]
                    print(f"✅ 找到 {compiler}: {version_line}")
                    return True
            except FileNotFoundError:
                continue
        
        print("❌ 未找到 C++ 编译器")
        print("   Linux: sudo apt-get install build-essential")
        print("   macOS: brew install gcc")
        return False


def check_dependencies():
    """检查 Python 依赖"""
    required_packages = ["numpy", "pybind11"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} 未安装")
    
    if missing_packages:
        print(f"\n请安装缺失的包:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True


def build_with_pyproject():
    """使用 pyproject.toml 构建"""
    print("\n🔨 使用 pyproject.toml 构建 C++ 扩展...")
    
    try:
        # 方法1: 使用 pip 构建（推荐）
        print("尝试使用 pip 构建...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--use-pep517", "-e", "."],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ 使用 pip 构建成功!")
            return True
        else:
            print("pip 构建失败，尝试其他方法...")
            print("错误输出:")
            print(result.stderr)
        
        # 方法2: 使用 build 包
        print("尝试使用 build 包构建...")
        try:
            import build
            print("✅ build 包可用")
            
            result = subprocess.run(
                [sys.executable, "-m", "build", "--wheel"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ 使用 build 构建成功!")
                return True
            else:
                print("build 构建失败")
                print("错误输出:")
                print(result.stderr)
                
        except ImportError:
            print("build 包不可用，跳过")
        
        # 方法3: 使用 setuptools
        print("尝试使用 setuptools 构建...")
        result = subprocess.run(
            [sys.executable, "-m", "setuptools", "build_ext", "--inplace"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ 使用 setuptools 构建成功!")
            return True
        else:
            print("❌ 所有构建方法都失败了!")
            print("错误输出:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 构建过程中出现错误: {e}")
        return False


def check_built_extension():
    """检查构建的扩展"""
    print("\n🔍 检查构建的扩展...")
    
    # 检查生成的文件
    transform_module = Path("src/pybase/_transform")
    if platform.system().lower() == "windows":
        transform_module = transform_module.with_suffix(".pyd")
    else:
        transform_module = transform_module.with_suffix(".so")
    
    if transform_module.exists():
        print(f"✅ 扩展模块已生成: {transform_module}")
        print(f"   文件大小: {transform_module.stat().st_size} 字节")
        return True
    else:
        print("❌ 扩展模块文件未找到")
        return False


def test_extension():
    """测试 C++ 扩展"""
    print("\n🧪 测试 C++ 扩展...")
    
    try:
        # 添加 src 目录到路径
        sys.path.insert(0, "src")
        
        from pybase.transform import get_cpp_availability, transform
        import numpy as np
        
        if get_cpp_availability():
            print("✅ C++ 扩展可用")
            
            # 简单功能测试
            test_dict = {"test": np.array([1.0, 2.0, 3.0])}
            result = transform(test_dict)
            
            if "test_new" in result:
                print("✅ Transform 功能测试通过")
                return True
            else:
                print("❌ Transform 功能测试失败")
                return False
        else:
            print("⚠️  C++ 扩展不可用，将使用 Python 回退实现")
            return True
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return False


def install_package():
    """安装包"""
    print("\n📦 安装包...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ 包安装成功!")
            return True
        else:
            print("❌ 包安装失败!")
            print("错误输出:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 安装过程中出现错误: {e}")
        return False


def run_example():
    """运行示例"""
    print("\n🚀 运行示例...")
    
    example_file = Path("examples/transform_example.py")
    if not example_file.exists():
        print("⚠️  示例文件不存在，跳过示例运行")
        return True
    
    try:
        result = subprocess.run(
            [sys.executable, str(example_file)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ 示例运行成功!")
            print("输出预览:")
            lines = result.stdout.split('\n')[:10]
            for line in lines:
                print(f"  {line}")
            if len(result.stdout.split('\n')) > 10:
                print("  ...")
            return True
        else:
            print("❌ 示例运行失败!")
            print("错误输出:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 运行示例时出现错误: {e}")
        return False


def show_build_info():
    """显示构建信息"""
    print("\n📋 构建信息:")
    print(f"   构建后端: setuptools.build_meta")
    print(f"   构建工具: pyproject.toml")
    print(f"   C++ 标准: C++17")
    print(f"   绑定框架: pybind11")
    print(f"   扩展模块: pybase._transform")


def main():
    """主函数"""
    print("PyBase 现代 C++ 扩展构建脚本")
    print("=" * 50)
    print("使用 pyproject.toml 和 PEP 517 标准")
    
    # 检查环境
    checks = [
        ("Python 版本", check_python_version),
        ("C++ 编译器", check_compiler),
        ("Python 依赖", check_dependencies),
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n检查 {name}...")
        if not check_func():
            all_passed = False
            break
    
    if not all_passed:
        print("\n❌ 环境检查失败，请解决上述问题后重试")
        return 1
    
    show_build_info()
    
    # 构建和测试
    steps = [
        ("构建 C++ 扩展", build_with_pyproject),
        ("检查扩展文件", check_built_extension),
        ("测试扩展", test_extension),
        ("安装包", install_package),
        ("运行示例", run_example),
    ]
    
    for name, step_func in steps:
        if not step_func():
            print(f"\n❌ {name} 失败")
            return 1
    
    print("\n🎉 所有步骤完成!")
    print("\n使用说明:")
    print("1. 导入模块: from pybase.transform import transform")
    print("2. 运行测试: pytest tests/test_transform.py")
    print("3. 查看示例: python examples/transform_example.py")
    print("\n现代构建方式:")
    print("1. pip install --use-pep517 -e .")
    print("2. python -m build --wheel")
    print("3. python -m setuptools build_ext --inplace")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 