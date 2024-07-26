// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from angbao_navigation2:msg/CustomDetection.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "angbao_navigation2/msg/detail/custom_detection__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace angbao_navigation2
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void CustomDetection_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) angbao_navigation2::msg::CustomDetection(_init);
}

void CustomDetection_fini_function(void * message_memory)
{
  auto typed_message = static_cast<angbao_navigation2::msg::CustomDetection *>(message_memory);
  typed_message->~CustomDetection();
}

size_t size_function__CustomDetection__anchors(const void * untyped_member)
{
  (void)untyped_member;
  return 4;
}

const void * get_const_function__CustomDetection__anchors(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::array<int32_t, 4> *>(untyped_member);
  return &member[index];
}

void * get_function__CustomDetection__anchors(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::array<int32_t, 4> *>(untyped_member);
  return &member[index];
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember CustomDetection_message_member_array[2] = {
  {
    "image",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<sensor_msgs::msg::Image>(),  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(angbao_navigation2::msg::CustomDetection, image),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "anchors",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    true,  // is array
    4,  // array size
    false,  // is upper bound
    offsetof(angbao_navigation2::msg::CustomDetection, anchors),  // bytes offset in struct
    nullptr,  // default value
    size_function__CustomDetection__anchors,  // size() function pointer
    get_const_function__CustomDetection__anchors,  // get_const(index) function pointer
    get_function__CustomDetection__anchors,  // get(index) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers CustomDetection_message_members = {
  "angbao_navigation2::msg",  // message namespace
  "CustomDetection",  // message name
  2,  // number of fields
  sizeof(angbao_navigation2::msg::CustomDetection),
  CustomDetection_message_member_array,  // message members
  CustomDetection_init_function,  // function to initialize message memory (memory has to be allocated)
  CustomDetection_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t CustomDetection_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &CustomDetection_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace angbao_navigation2


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<angbao_navigation2::msg::CustomDetection>()
{
  return &::angbao_navigation2::msg::rosidl_typesupport_introspection_cpp::CustomDetection_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, angbao_navigation2, msg, CustomDetection)() {
  return &::angbao_navigation2::msg::rosidl_typesupport_introspection_cpp::CustomDetection_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
