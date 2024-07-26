// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from angbao_navigation2:msg/CustomDetection.idl
// generated code does not contain a copyright notice

#ifndef ANGBAO_NAVIGATION2__MSG__DETAIL__CUSTOM_DETECTION__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define ANGBAO_NAVIGATION2__MSG__DETAIL__CUSTOM_DETECTION__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "angbao_navigation2/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "angbao_navigation2/msg/detail/custom_detection__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace angbao_navigation2
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_angbao_navigation2
cdr_serialize(
  const angbao_navigation2::msg::CustomDetection & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_angbao_navigation2
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  angbao_navigation2::msg::CustomDetection & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_angbao_navigation2
get_serialized_size(
  const angbao_navigation2::msg::CustomDetection & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_angbao_navigation2
max_serialized_size_CustomDetection(
  bool & full_bounded,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace angbao_navigation2

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_angbao_navigation2
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, angbao_navigation2, msg, CustomDetection)();

#ifdef __cplusplus
}
#endif

#endif  // ANGBAO_NAVIGATION2__MSG__DETAIL__CUSTOM_DETECTION__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
