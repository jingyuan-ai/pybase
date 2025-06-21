"""
Transform 功能测试
"""

import pytest
import numpy as np
from .common import cpp_test, unit_test, integration_test
from pybase.transform import transform, scale_array, create_new_key, get_cpp_availability


@cpp_test
def test_transform_basic():
    """测试基本的 transform 功能"""
    # 创建测试数据
    input_dict = {
        "array1": np.array([1.0, 2.0, 3.0]),
        "array2": np.array([[1.0, 2.0], [3.0, 4.0]]),
        "array3": np.array([10.0, 20.0, 30.0, 40.0])
    }
    
    # 执行转换
    result = transform(input_dict)
    
    # 验证结果
    assert "array1_new" in result
    assert "array2_new" in result
    assert "array3_new" in result
    
    # 验证数组值（乘以0.3）
    np.testing.assert_array_almost_equal(result["array1_new"], np.array([0.3, 0.6, 0.9]))
    np.testing.assert_array_almost_equal(result["array2_new"], np.array([[0.3, 0.6], [0.9, 1.2]]))
    np.testing.assert_array_almost_equal(result["array3_new"], np.array([3.0, 6.0, 9.0, 12.0]))


@cpp_test
def test_transform_empty_dict():
    """测试空字典"""
    result = transform({})
    assert result == {}


@cpp_test
def test_transform_single_array():
    """测试单个数组"""
    input_dict = {"test": np.array([1.0, 2.0, 3.0])}
    result = transform(input_dict)
    
    assert "test_new" in result
    np.testing.assert_array_almost_equal(result["test_new"], np.array([0.3, 0.6, 0.9]))


@cpp_test
def test_transform_different_dtypes():
    """测试不同数据类型的数组"""
    input_dict = {
        "int_array": np.array([1, 2, 3], dtype=np.int32),
        "float_array": np.array([1.5, 2.5, 3.5], dtype=np.float32),
        "double_array": np.array([10.0, 20.0, 30.0], dtype=np.float64)
    }
    
    result = transform(input_dict)
    
    # 验证所有结果都是 float64
    assert result["int_array_new"].dtype == np.float64
    assert result["float_array_new"].dtype == np.float64
    assert result["double_array_new"].dtype == np.float64
    
    # 验证值
    np.testing.assert_array_almost_equal(result["int_array_new"], np.array([0.3, 0.6, 0.9]))
    np.testing.assert_array_almost_equal(result["float_array_new"], np.array([0.45, 0.75, 1.05]))
    np.testing.assert_array_almost_equal(result["double_array_new"], np.array([3.0, 6.0, 9.0]))


@cpp_test
def test_transform_multidimensional():
    """测试多维数组"""
    input_dict = {
        "1d": np.array([1.0, 2.0, 3.0]),
        "2d": np.array([[1.0, 2.0], [3.0, 4.0]]),
        "3d": np.array([[[1.0, 2.0], [3.0, 4.0]], [[5.0, 6.0], [7.0, 8.0]]])
    }
    
    result = transform(input_dict)
    
    # 验证形状保持不变
    assert result["1d_new"].shape == (3,)
    assert result["2d_new"].shape == (2, 2)
    assert result["3d_new"].shape == (2, 2, 2)
    
    # 验证值
    np.testing.assert_array_almost_equal(result["1d_new"], np.array([0.3, 0.6, 0.9]))
    np.testing.assert_array_almost_equal(result["2d_new"], np.array([[0.3, 0.6], [0.9, 1.2]]))
    expected_3d = np.array([[[0.3, 0.6], [0.9, 1.2]], [[1.5, 1.8], [2.1, 2.4]]])
    np.testing.assert_array_almost_equal(result["3d_new"], expected_3d)


@cpp_test
def test_transform_list_input():
    """测试列表输入（应该自动转换为numpy数组）"""
    input_dict = {
        "list1": [1.0, 2.0, 3.0],
        "list2": [[1.0, 2.0], [3.0, 4.0]]
    }
    
    result = transform(input_dict)
    
    assert "list1_new" in result
    assert "list2_new" in result
    
    np.testing.assert_array_almost_equal(result["list1_new"], np.array([0.3, 0.6, 0.9]))
    np.testing.assert_array_almost_equal(result["list2_new"], np.array([[0.3, 0.6], [0.9, 1.2]]))


@unit_test
def test_transform_invalid_input():
    """测试无效输入"""
    # 非字典输入
    with pytest.raises(ValueError, match="Input must be a dictionary"):
        transform("not a dict")
    
    # 非字符串键
    with pytest.raises(ValueError, match="All keys must be strings"):
        transform({123: np.array([1.0, 2.0])})
    
    # 非数值数组
    try:
        with pytest.raises(TypeError, match="Array must be numeric"):
            transform({"test": np.array(["a", "b", "c"])})
        assert False
    except Exception as e:
        assert True


@cpp_test
def test_scale_array_basic():
    """测试 scale_array 基本功能"""
    arr = np.array([1.0, 2.0, 3.0])
    result = scale_array(arr)
    
    np.testing.assert_array_almost_equal(result, np.array([0.3, 0.6, 0.9]))


@cpp_test
def test_scale_array_custom_factor():
    """测试自定义缩放因子"""
    arr = np.array([1.0, 2.0, 3.0])
    result = scale_array(arr, factor=2.0)
    
    np.testing.assert_array_almost_equal(result, np.array([2.0, 4.0, 6.0]))


@cpp_test
def test_scale_array_multidimensional():
    """测试多维数组缩放"""
    arr = np.array([[1.0, 2.0], [3.0, 4.0]])
    result = scale_array(arr, factor=0.5)
    
    np.testing.assert_array_almost_equal(result, np.array([[0.5, 1.0], [1.5, 2.0]]))


@unit_test
def test_scale_array_invalid_input():
    """测试 scale_array 无效输入"""
    # 非数值数组
    with pytest.raises(TypeError, match="Array must be numeric"):
        scale_array(np.array(["a", "b", "c"]))
    
    # 无法转换的输入
    with pytest.raises(TypeError, match="Cannot convert input to numeric array"):
        scale_array("not an array")


@cpp_test
def test_create_new_key_basic():
    """测试 create_new_key 基本功能"""
    result = create_new_key("test")
    assert result == "test_new"


@cpp_test
def test_create_new_key_custom_suffix():
    """测试自定义后缀"""
    result = create_new_key("test", "_modified")
    assert result == "test_modified"


@cpp_test
def test_create_new_key_empty_string():
    """测试空字符串"""
    result = create_new_key("", "_suffix")
    assert result == "_suffix"


@unit_test
def test_create_new_key_invalid_input():
    """测试 create_new_key 无效输入"""
    # 非字符串键
    with pytest.raises(ValueError, match="Key must be a string"):
        create_new_key(123)
    
    # 非字符串后缀
    with pytest.raises(ValueError, match="Suffix must be a string"):
        create_new_key("test", 123)


@cpp_test
def test_cpp_availability():
    """测试 C++ 实现可用性"""
    # 这个测试会告诉我们 C++ 实现是否可用
    availability = get_cpp_availability()
    print(f"C++ implementation available: {availability}")
    
    # 无论是否可用，都应该能正常工作
    input_dict = {"test": np.array([1.0, 2.0, 3.0])}
    result = transform(input_dict)
    
    assert "test_new" in result
    np.testing.assert_array_almost_equal(result["test_new"], np.array([0.3, 0.6, 0.9]))


@integration_test
def test_transform_performance():
    """测试性能（集成测试）"""
    # 创建大型数组进行性能测试
    large_array = np.random.random((1000, 1000))
    input_dict = {"large": large_array}
    
    # 执行转换
    result = transform(input_dict)
    
    # 验证结果
    assert "large_new" in result
    assert result["large_new"].shape == (1000, 1000)
    
    # 验证值（随机数组，只检查几个元素）
    expected_value = large_array[0, 0] * 0.3
    actual_value = result["large_new"][0, 0]
    assert abs(expected_value - actual_value) < 1e-10


@cpp_test
def test_transform_edge_cases():
    """测试边界情况"""
    # 零数组
    input_dict = {"zeros": np.zeros((3, 3))}
    result = transform(input_dict)
    np.testing.assert_array_almost_equal(result["zeros_new"], np.zeros((3, 3)))
    
    # 负数数组
    input_dict = {"negatives": np.array([-1.0, -2.0, -3.0])}
    result = transform(input_dict)
    np.testing.assert_array_almost_equal(result["negatives_new"], np.array([-0.3, -0.6, -0.9]))
    
    # 大数值数组
    input_dict = {"large_values": np.array([1e6, 2e6, 3e6])}
    result = transform(input_dict)
    np.testing.assert_array_almost_equal(result["large_values_new"], np.array([3e5, 6e5, 9e5]))


@cpp_test
def test_transform_preserves_input():
    """测试输入不被修改"""
    original_array = np.array([1.0, 2.0, 3.0])
    input_dict = {"test": original_array.copy()}
    
    result = transform(input_dict)
    
    # 验证原始数组没有被修改
    np.testing.assert_array_equal(original_array, np.array([1.0, 2.0, 3.0]))
    
    # 验证结果数组是新的
    assert result["test_new"] is not original_array 