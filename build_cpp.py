#!/usr/bin/env python3
"""
C++ 扩展构建脚本

自动检测环境并构建 C++ Transform 模块
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


def build_extension():
    """构建 C++ 扩展"""
    print("\n🔨 开始构建 C++ 扩展...")
    
    try:
        # 使用 setup.py 构建
        result = subprocess.run(
            [sys.executable, "setup.py", "build_ext", "--inplace"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ C++ 扩展构建成功!")
            
            # 检查生成的文件
            transform_module = Path("src/pybase/_transform")
            if platform.system().lower() == "windows":
                transform_module = transform_module.with_suffix(".pyd")
            else:
                transform_module = transform_module.with_suffix(".so")
            
            if transform_module.exists():
                print(f"✅ 扩展模块已生成: {transform_module}")
            else:
                print("⚠️  扩展模块文件未找到")
            
            return True
        else:
            print("❌ 构建失败!")
            print("错误输出:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 构建过程中出现错误: {e}")
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


def main():
    """主函数"""
    print("PyBase C++ 扩展构建脚本")
    print("=" * 50)
    
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
    
    # 构建和测试
    steps = [
        ("构建 C++ 扩展", build_extension),
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
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 