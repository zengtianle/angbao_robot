// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from angbao_navigation2:msg/CustomDetection.idl
// generated code does not contain a copyright notice

#ifndef ANGBAO_NAVIGATION2__MSG__DETAIL__CUSTOM_DETECTION__TRAITS_HPP_
#define ANGBAO_NAVIGATION2__MSG__DETAIL__CUSTOM_DETECTION__TRAITS_HPP_

#include "angbao_navigation2/msg/detail/custom_detection__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

// Include directives for member types
// Member 'image'
#include "sensor_msgs/msg/detail/image__traits.hpp"

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<angbao_navigation2::msg::CustomDetection>()
{
  return "angbao_navigation2::msg::CustomDetection";
}

template<>
inline const char * name<angbao_navigation2::msg::CustomDetection>()
{
  return "angbao_navigation2/msg/CustomDetection";
}

template<>
struct has_fixed_size<angbao_navigation2::msg::CustomDetection>
  : std::integral_constant<bool, has_fixed_size<sensor_msgs::msg::Image>::value> {};

template<>
struct has_bounded_size<angbao_navigation2::msg::CustomDetection>
  : std::integral_constant<bool, has_bounded_size<sensor_msgs::msg::Image>::value> {};

template<>
struct is_message<angbao_navigation2::msg::CustomDetection>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ANGBAO_NAVIGATION2__MSG__DETAIL__CUSTOM_DETECTION__TRAITS_HPP_
