#!/usr/bin/env python3
"""
Setup script for PyBase with C++ extensions

This file is needed because pyproject.toml has limited support for C++ extensions.
The main configuration is in pyproject.toml, but C++ extensions are defined here.
"""

from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext
import numpy as np

# Define the C++ extension
ext_modules = [
    Pybind11Extension(
        "pybase._transform",
        ["src/pybase/transform_binding.cpp", "src/pybase/transform.cpp"],
        include_dirs=[np.get_include()],
        language='c++',
        cxx_std=17,  # Use C++17 standard
    ),
]

# Setup configuration - most config is in pyproject.toml
setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,  # Required for C++ extensions
) 