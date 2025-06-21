"""
简单测试文件
"""

def test_simple():
    """简单的测试"""
    assert 1 + 1 == 2


def test_string():
    """字符串测试"""
    assert "hello" in "hello world"


def test_list():
    """列表测试"""
    numbers = [1, 2, 3, 4, 5]
    assert len(numbers) == 5
    assert 3 in numbers 