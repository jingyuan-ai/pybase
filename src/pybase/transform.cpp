#include "transform.h"
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <string>
#include <map>
#include <vector>
#include <algorithm>
#include <stdexcept>

namespace py = pybind11;

namespace pybase {

std::map<std::string, py::array_t<double>> transform(
    const std::map<std::string, py::array_t<double>>& input_dict
) {
    std::map<std::string, py::array_t<double>> output_dict;
    
    for (const auto& pair : input_dict) {
        const std::string& key = pair.first;
        const py::array_t<double>& arr = pair.second;
        
        // Create new key by appending "_new"
        std::string new_key = create_new_key(key);
        
        // Scale the array by 0.3
        py::array_t<double> scaled_arr = scale_array(arr, 0.3);
        
        // Add to output dictionary
        output_dict[new_key] = scaled_arr;
    }
    
    return output_dict;
}

py::array_t<double> scale_array(
    const py::array_t<double>& arr,
    double factor
) {
    // Get array info
    py::buffer_info buf = arr.request();
    
    if (buf.ndim == 0) {
        throw std::runtime_error("Zero-dimensional arrays are not supported");
    }
    
    // Create output array with same shape
    py::array_t<double> result(buf.shape);
    py::buffer_info result_buf = result.request();
    
    // Get pointers to data
    double* input_ptr = static_cast<double*>(buf.ptr);
    double* output_ptr = static_cast<double*>(result_buf.ptr);
    
    // Get total size
    size_t total_size = 1;
    for (size_t i = 0; i < buf.ndim; ++i) {
        total_size *= buf.shape[i];
    }
    
    // Scale each element
    for (size_t i = 0; i < total_size; ++i) {
        output_ptr[i] = input_ptr[i] * factor;
    }
    
    return result;
}

std::string create_new_key(const std::string& key, const std::string& suffix) {
    return key + suffix;
}

} // namespace pybase 