#ifndef PYBASE_TRANSFORM_H
#define PYBASE_TRANSFORM_H

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <string>
#include <map>
#include <vector>

namespace py = pybind11;

namespace pybase {

/**
 * Transform function that processes numpy arrays
 * 
 * @param input_dict Input dictionary with string keys and numpy array values
 * @return Output dictionary with modified keys and scaled arrays
 */
std::map<std::string, py::array_t<double>> transform(
    const std::map<std::string, py::array_t<double>>& input_dict
);

/**
 * Scale a numpy array by a factor
 * 
 * @param arr Input numpy array
 * @param factor Scaling factor
 * @return Scaled numpy array
 */
py::array_t<double> scale_array(
    const py::array_t<double>& arr,
    double factor = 0.3
);

/**
 * Create a new key by appending suffix
 * 
 * @param key Original key
 * @param suffix Suffix to append
 * @return New key
 */
std::string create_new_key(const std::string& key, const std::string& suffix = "_new");

} // namespace pybase

#endif // PYBASE_TRANSFORM_H 