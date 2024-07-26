// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from angbao_navigation2:msg/CustomDetection.idl
// generated code does not contain a copyright notice

#ifndef ANGBAO_NAVIGATION2__MSG__DETAIL__CUSTOM_DETECTION__BUILDER_HPP_
#define ANGBAO_NAVIGATION2__MSG__DETAIL__CUSTOM_DETECTION__BUILDER_HPP_

#include "angbao_navigation2/msg/detail/custom_detection__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace angbao_navigation2
{

namespace msg
{

namespace builder
{

class Init_CustomDetection_anchors
{
public:
  explicit Init_CustomDetection_anchors(::angbao_navigation2::msg::CustomDetection & msg)
  : msg_(msg)
  {}
  ::angbao_navigation2::msg::CustomDetection anchors(::angbao_navigation2::msg::CustomDetection::_anchors_type arg)
  {
    msg_.anchors = std::move(arg);
    return std::move(msg_);
  }

private:
  ::angbao_navigation2::msg::CustomDetection msg_;
};

class Init_CustomDetection_image
{
public:
  Init_CustomDetection_image()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CustomDetection_anchors image(::angbao_navigation2::msg::CustomDetection::_image_type arg)
  {
    msg_.image = std::move(arg);
    return Init_CustomDetection_anchors(msg_);
  }

private:
  ::angbao_navigation2::msg::CustomDetection msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::angbao_navigation2::msg::CustomDetection>()
{
  return angbao_navigation2::msg::builder::Init_CustomDetection_image();
}

}  // namespace angbao_navigation2

#endif  // ANGBAO_NAVIGATION2__MSG__DETAIL__CUSTOM_DETECTION__BUILDER_HPP_
