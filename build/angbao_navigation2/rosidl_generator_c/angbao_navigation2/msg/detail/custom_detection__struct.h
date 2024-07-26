// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from angbao_navigation2:msg/CustomDetection.idl
// generated code does not contain a copyright notice

#ifndef ANGBAO_NAVIGATION2__MSG__DETAIL__CUSTOM_DETECTION__STRUCT_H_
#define ANGBAO_NAVIGATION2__MSG__DETAIL__CUSTOM_DETECTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'image'
#include "sensor_msgs/msg/detail/image__struct.h"

// Struct defined in msg/CustomDetection in the package angbao_navigation2.
typedef struct angbao_navigation2__msg__CustomDetection
{
  sensor_msgs__msg__Image image;
  int32_t anchors[4];
} angbao_navigation2__msg__CustomDetection;

// Struct for a sequence of angbao_navigation2__msg__CustomDetection.
typedef struct angbao_navigation2__msg__CustomDetection__Sequence
{
  angbao_navigation2__msg__CustomDetection * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} angbao_navigation2__msg__CustomDetection__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ANGBAO_NAVIGATION2__MSG__DETAIL__CUSTOM_DETECTION__STRUCT_H_
