#!/usr/bin/env python3
"""
Transform 功能使用示例

演示如何使用 C++ 实现的 transform 接口
"""

import numpy as np
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pybase.transform import transform, scale_array, create_new_key, get_cpp_availability


def basic_example():
    """基本使用示例"""
    print("=== 基本使用示例 ===")
    
    # 创建测试数据
    input_dict = {
        "array1": np.array([1.0, 2.0, 3.0]),
        "array2": np.array([[1.0, 2.0], [3.0, 4.0]]),
        "array3": np.array([10.0, 20.0, 30.0, 40.0])
    }
    
    print("输入字典:")
    for key, value in input_dict.items():
        print(f"  {key}: {value}")
    
    # 执行转换
    result = transform(input_dict)
    
    print("\n输出字典:")
    for key, value in result.items():
        print(f"  {key}: {value}")
    
    print(f"\nC++ 实现可用: {get_cpp_availability()}")


def different_dtypes_example():
    """不同数据类型示例"""
    print("\n=== 不同数据类型示例 ===")
    
    input_dict = {
        "int_array": np.array([1, 2, 3], dtype=np.int32),
        "float_array": np.array([1.5, 2.5, 3.5], dtype=np.float32),
        "double_array": np.array([10.0, 20.0, 30.0], dtype=np.float64)
    }
    
    print("输入字典:")
    for key, value in input_dict.items():
        print(f"  {key}: {value} (dtype: {value.dtype})")
    
    result = transform(input_dict)
    
    print("\n输出字典:")
    for key, value in result.items():
        print(f"  {key}: {value} (dtype: {value.dtype})")


def multidimensional_example():
    """多维数组示例"""
    print("\n=== 多维数组示例 ===")
    
    input_dict = {
        "1d": np.array([1.0, 2.0, 3.0]),
        "2d": np.array([[1.0, 2.0], [3.0, 4.0]]),
        "3d": np.array([[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]])
    }
    
    print("输入字典:")
    for key, value in input_dict.items():
        print(f"  {key}: shape={value.shape}, value={value}")
    
    result = transform(input_dict)
    
    print("\n输出字典:")
    for key, value in result.items():
        print(f"  {key}: shape={value.shape}, value={value}")


def list_input_example():
    """列表输入示例"""
    print("\n=== 列表输入示例 ===")
    
    input_dict = {
        "list1": [1.0, 2.0, 3.0],
        "list2": [[1.0, 2.0], [3.0, 4.0]]
    }
    
    print("输入字典:")
    for key, value in input_dict.items():
        print(f"  {key}: {value} (type: {type(value)})")
    
    result = transform(input_dict)
    
    print("\n输出字典:")
    for key, value in result.items():
        print(f"  {key}: {value} (type: {type(value)})")


def scale_array_example():
    """scale_array 函数示例"""
    print("\n=== scale_array 函数示例 ===")
    
    # 基本用法
    arr1 = np.array([1.0, 2.0, 3.0])
    result1 = scale_array(arr1)
    print(f"原始数组: {arr1}")
    print(f"缩放后 (默认0.3): {result1}")
    
    # 自定义缩放因子
    arr2 = np.array([[1.0, 2.0], [3.0, 4.0]])
    result2 = scale_array(arr2, factor=2.0)
    print(f"\n原始数组: {arr2}")
    print(f"缩放后 (因子2.0): {result2}")


def create_new_key_example():
    """create_new_key 函数示例"""
    print("\n=== create_new_key 函数示例 ===")
    
    # 基本用法
    key1 = "test"
    new_key1 = create_new_key(key1)
    print(f"原始键: '{key1}' -> 新键: '{new_key1}'")
    
    # 自定义后缀
    key2 = "data"
    new_key2 = create_new_key(key2, "_processed")
    print(f"原始键: '{key2}' -> 新键: '{new_key2}'")


def performance_comparison():
    """性能对比示例"""
    print("\n=== 性能对比示例 ===")
    
    import time
    
    # 创建大型数组
    large_array = np.random.random((1000, 1000))
    input_dict = {"large": large_array}
    
    # 测试 transform 性能
    start_time = time.time()
    result = transform(input_dict)
    end_time = time.time()
    
    print(f"处理 1000x1000 数组耗时: {end_time - start_time:.4f} 秒")
    print(f"结果形状: {result['large_new'].shape}")
    
    # 验证结果正确性
    expected_value = large_array[0, 0] * 0.3
    actual_value = result['large_new'][0, 0]
    print(f"结果验证: 期望 {expected_value:.6f}, 实际 {actual_value:.6f}")
    print(f"误差: {abs(expected_value - actual_value):.2e}")


def error_handling_example():
    """错误处理示例"""
    print("\n=== 错误处理示例 ===")
    
    # 测试无效输入
    test_cases = [
        ("非字典输入", "not a dict"),
        ("非字符串键", {123: np.array([1.0, 2.0])}),
        ("非数值数组", {"test": np.array(["a", "b", "c"])}),
    ]
    
    for description, test_input in test_cases:
        print(f"\n测试: {description}")
        try:
            result = transform(test_input)
            print(f"  结果: {result}")
        except Exception as e:
            print(f"  错误: {type(e).__name__}: {e}")


def main():
    """主函数"""
    print("PyBase Transform 功能演示")
    print("=" * 50)
    
    # 检查 C++ 实现可用性
    cpp_available = get_cpp_availability()
    print(f"C++ 实现可用: {cpp_available}")
    print()
    
    # 运行示例
    basic_example()
    different_dtypes_example()
    multidimensional_example()
    list_input_example()
    scale_array_example()
    create_new_key_example()
    performance_comparison()
    error_handling_example()
    
    print("\n" + "=" * 50)
    print("演示完成！")


if __name__ == "__main__":
    main() 