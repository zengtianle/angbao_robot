// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from angbao_navigation2:msg/CustomDetection.idl
// generated code does not contain a copyright notice

#ifndef ANGBAO_NAVIGATION2__MSG__DETAIL__CUSTOM_DETECTION__STRUCT_HPP_
#define ANGBAO_NAVIGATION2__MSG__DETAIL__CUSTOM_DETECTION__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


// Include directives for member types
// Member 'image'
#include "sensor_msgs/msg/detail/image__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__angbao_navigation2__msg__CustomDetection __attribute__((deprecated))
#else
# define DEPRECATED__angbao_navigation2__msg__CustomDetection __declspec(deprecated)
#endif

namespace angbao_navigation2
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CustomDetection_
{
  using Type = CustomDetection_<ContainerAllocator>;

  explicit CustomDetection_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : image(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<int32_t, 4>::iterator, int32_t>(this->anchors.begin(), this->anchors.end(), 0l);
    }
  }

  explicit CustomDetection_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : image(_alloc, _init),
    anchors(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<int32_t, 4>::iterator, int32_t>(this->anchors.begin(), this->anchors.end(), 0l);
    }
  }

  // field types and members
  using _image_type =
    sensor_msgs::msg::Image_<ContainerAllocator>;
  _image_type image;
  using _anchors_type =
    std::array<int32_t, 4>;
  _anchors_type anchors;

  // setters for named parameter idiom
  Type & set__image(
    const sensor_msgs::msg::Image_<ContainerAllocator> & _arg)
  {
    this->image = _arg;
    return *this;
  }
  Type & set__anchors(
    const std::array<int32_t, 4> & _arg)
  {
    this->anchors = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    angbao_navigation2::msg::CustomDetection_<ContainerAllocator> *;
  using ConstRawPtr =
    const angbao_navigation2::msg::CustomDetection_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<angbao_navigation2::msg::CustomDetection_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<angbao_navigation2::msg::CustomDetection_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      angbao_navigation2::msg::CustomDetection_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<angbao_navigation2::msg::CustomDetection_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      angbao_navigation2::msg::CustomDetection_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<angbao_navigation2::msg::CustomDetection_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<angbao_navigation2::msg::CustomDetection_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<angbao_navigation2::msg::CustomDetection_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__angbao_navigation2__msg__CustomDetection
    std::shared_ptr<angbao_navigation2::msg::CustomDetection_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__angbao_navigation2__msg__CustomDetection
    std::shared_ptr<angbao_navigation2::msg::CustomDetection_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CustomDetection_ & other) const
  {
    if (this->image != other.image) {
      return false;
    }
    if (this->anchors != other.anchors) {
      return false;
    }
    return true;
  }
  bool operator!=(const CustomDetection_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CustomDetection_

// alias to use template instance with default allocator
using CustomDetection =
  angbao_navigation2::msg::CustomDetection_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace angbao_navigation2

#endif  // ANGBAO_NAVIGATION2__MSG__DETAIL__CUSTOM_DETECTION__STRUCT_HPP_
