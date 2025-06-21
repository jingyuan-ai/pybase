"""
PyBase Transform Module

Provides high-level interface for transforming numpy arrays using C++ backend.
"""

import numpy as np
from typing import Dict, Union, Any
import warnings

try:
    from . import _transform
    _CPP_AVAILABLE = True
except ImportError:
    _CPP_AVAILABLE = False
    warnings.warn("C++ transform module not available. Using Python fallback.")


def transform(input_dict: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    """
    Transform input dictionary by scaling numpy arrays by 0.3.
    
    Args:
        input_dict: Dictionary with string keys and numpy array values
        
    Returns:
        Dictionary with modified keys (original + "_new") and scaled arrays
        
    Raises:
        ValueError: If input is not a dictionary or contains invalid arrays
        TypeError: If arrays are not numeric
    """
    # Input validation
    if not isinstance(input_dict, dict):
        raise ValueError("Input must be a dictionary")
    
    if not input_dict:
        return {}
    
    # Validate and convert arrays
    validated_dict = {}
    for key, value in input_dict.items():
        if not isinstance(key, str):
            raise ValueError(f"All keys must be strings, got {type(key)}")
        
        # Convert to numpy array if needed
        if not isinstance(value, np.ndarray):
            try:
                value = np.asarray(value, dtype=np.float64)
            except (ValueError, TypeError) as e:
                raise TypeError(f"Value for key '{key}' cannot be converted to numeric array: {e}")
        
        # Ensure array is numeric
        if not np.issubdtype(value.dtype, np.number):
            raise TypeError(f"Array for key '{key}' must be numeric, got {value.dtype}")
        
        # Convert to double precision
        validated_dict[key] = value.astype(np.float64)
    
    # Use C++ implementation if available
    if _CPP_AVAILABLE:
        try:
            return _transform.transform(validated_dict)
        except Exception as e:
            warnings.warn(f"C++ transform failed, falling back to Python: {e}")
            return _python_transform(validated_dict)
    else:
        return _python_transform(validated_dict)


def _python_transform(input_dict: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    """
    Python fallback implementation of transform function.
    
    Args:
        input_dict: Validated dictionary with numpy arrays
        
    Returns:
        Transformed dictionary
    """
    raise NotImplementedError("Python transform is not implemented")
    output_dict = {}
    
    for key, arr in input_dict.items():
        # Create new key
        new_key = key + "_new"
        
        # Scale array by 0.3
        scaled_arr = arr * 0.3
        
        output_dict[new_key] = scaled_arr
    
    return output_dict


def scale_array(arr: np.ndarray, factor: float = 0.3) -> np.ndarray:
    """
    Scale a numpy array by a factor.
    
    Args:
        arr: Input numpy array
        factor: Scaling factor (default: 0.3)
        
    Returns:
        Scaled numpy array
        
    Raises:
        ValueError: If input is not a valid array
        TypeError: If array is not numeric
    """
    # Input validation
    if not isinstance(arr, np.ndarray):
        try:
            arr = np.asarray(arr, dtype=np.float64)
        except (ValueError, TypeError) as e:
            raise TypeError(f"Cannot convert input to numeric array: {e}")
    
    if not np.issubdtype(arr.dtype, np.number):
        raise TypeError(f"Array must be numeric, got {arr.dtype}")
    
    # Use C++ implementation if available
    if _CPP_AVAILABLE:
        try:
            return _transform.scale_array(arr.astype(np.float64), factor)
        except Exception as e:
            warnings.warn(f"C++ scale_array failed, falling back to Python: {e}")
            return arr * factor
    else:
        return arr * factor


def create_new_key(key: str, suffix: str = "_new") -> str:
    """
    Create a new key by appending suffix.
    
    Args:
        key: Original key
        suffix: Suffix to append (default: "_new")
        
    Returns:
        New key
        
    Raises:
        ValueError: If key is not a string
    """
    if not isinstance(key, str):
        raise ValueError(f"Key must be a string, got {type(key)}")
    
    if not isinstance(suffix, str):
        raise ValueError(f"Suffix must be a string, got {type(suffix)}")
    
    # Use C++ implementation if available
    if _CPP_AVAILABLE:
        try:
            return _transform.create_new_key(key, suffix)
        except Exception as e:
            warnings.warn(f"C++ create_new_key failed, falling back to Python: {e}")
            return key + suffix
    else:
        return key + suffix


# Version and availability info
__version__ = "1.0.0"
__author__ = "damon"

def get_cpp_availability() -> bool:
    """Check if C++ implementation is available."""
    return _CPP_AVAILABLE


def get_version() -> str:
    """Get the version of the transform module."""
    return __version__


# Example usage
if __name__ == "__main__":
    # Example usage
    import numpy as np
    
    # Create test data
    test_dict = {
        "array1": np.array([1.0, 2.0, 3.0]),
        "array2": np.array([[1.0, 2.0], [3.0, 4.0]]),
        "array3": np.array([10.0, 20.0, 30.0, 40.0])
    }
    
    print("Input dictionary:")
    for key, value in test_dict.items():
        print(f"  {key}: {value}")
    
    # Transform
    result = transform(test_dict)
    
    print("\nOutput dictionary:")
    for key, value in result.items():
        print(f"  {key}: {value}")
    
    print(f"\nC++ implementation available: {get_cpp_availability()}")
    print(f"Version: {get_version()}") 