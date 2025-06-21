#include "transform.h"
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(_transform, m) {
    m.doc() = "PyBase C++ Transform Module"; // Optional module docstring
    
    // Bind the transform function
    m.def("transform", &pybase::transform, 
          "Transform input dictionary by scaling numpy arrays by 0.3",
          py::arg("input_dict"));
    
    // Bind the scale_array function
    m.def("scale_array", &pybase::scale_array,
          "Scale a numpy array by a factor",
          py::arg("arr"), py::arg("factor") = 0.3);
    
    // Bind the create_new_key function
    m.def("create_new_key", &pybase::create_new_key,
          "Create a new key by appending suffix",
          py::arg("key"), py::arg("suffix") = "_new");
    
    // Add module attributes
    m.attr("__version__") = "1.0.0";
    m.attr("__author__") = "damon";
} 