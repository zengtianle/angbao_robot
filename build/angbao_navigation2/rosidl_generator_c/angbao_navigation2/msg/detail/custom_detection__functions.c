// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from angbao_navigation2:msg/CustomDetection.idl
// generated code does not contain a copyright notice
#include "angbao_navigation2/msg/detail/custom_detection__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `image`
#include "sensor_msgs/msg/detail/image__functions.h"

bool
angbao_navigation2__msg__CustomDetection__init(angbao_navigation2__msg__CustomDetection * msg)
{
  if (!msg) {
    return false;
  }
  // image
  if (!sensor_msgs__msg__Image__init(&msg->image)) {
    angbao_navigation2__msg__CustomDetection__fini(msg);
    return false;
  }
  // anchors
  return true;
}

void
angbao_navigation2__msg__CustomDetection__fini(angbao_navigation2__msg__CustomDetection * msg)
{
  if (!msg) {
    return;
  }
  // image
  sensor_msgs__msg__Image__fini(&msg->image);
  // anchors
}

bool
angbao_navigation2__msg__CustomDetection__are_equal(const angbao_navigation2__msg__CustomDetection * lhs, const angbao_navigation2__msg__CustomDetection * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // image
  if (!sensor_msgs__msg__Image__are_equal(
      &(lhs->image), &(rhs->image)))
  {
    return false;
  }
  // anchors
  for (size_t i = 0; i < 4; ++i) {
    if (lhs->anchors[i] != rhs->anchors[i]) {
      return false;
    }
  }
  return true;
}

bool
angbao_navigation2__msg__CustomDetection__copy(
  const angbao_navigation2__msg__CustomDetection * input,
  angbao_navigation2__msg__CustomDetection * output)
{
  if (!input || !output) {
    return false;
  }
  // image
  if (!sensor_msgs__msg__Image__copy(
      &(input->image), &(output->image)))
  {
    return false;
  }
  // anchors
  for (size_t i = 0; i < 4; ++i) {
    output->anchors[i] = input->anchors[i];
  }
  return true;
}

angbao_navigation2__msg__CustomDetection *
angbao_navigation2__msg__CustomDetection__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  angbao_navigation2__msg__CustomDetection * msg = (angbao_navigation2__msg__CustomDetection *)allocator.allocate(sizeof(angbao_navigation2__msg__CustomDetection), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(angbao_navigation2__msg__CustomDetection));
  bool success = angbao_navigation2__msg__CustomDetection__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
angbao_navigation2__msg__CustomDetection__destroy(angbao_navigation2__msg__CustomDetection * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    angbao_navigation2__msg__CustomDetection__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
angbao_navigation2__msg__CustomDetection__Sequence__init(angbao_navigation2__msg__CustomDetection__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  angbao_navigation2__msg__CustomDetection * data = NULL;

  if (size) {
    data = (angbao_navigation2__msg__CustomDetection *)allocator.zero_allocate(size, sizeof(angbao_navigation2__msg__CustomDetection), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = angbao_navigation2__msg__CustomDetection__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        angbao_navigation2__msg__CustomDetection__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
angbao_navigation2__msg__CustomDetection__Sequence__fini(angbao_navigation2__msg__CustomDetection__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      angbao_navigation2__msg__CustomDetection__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

angbao_navigation2__msg__CustomDetection__Sequence *
angbao_navigation2__msg__CustomDetection__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  angbao_navigation2__msg__CustomDetection__Sequence * array = (angbao_navigation2__msg__CustomDetection__Sequence *)allocator.allocate(sizeof(angbao_navigation2__msg__CustomDetection__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = angbao_navigation2__msg__CustomDetection__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
angbao_navigation2__msg__CustomDetection__Sequence__destroy(angbao_navigation2__msg__CustomDetection__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    angbao_navigation2__msg__CustomDetection__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
angbao_navigation2__msg__CustomDetection__Sequence__are_equal(const angbao_navigation2__msg__CustomDetection__Sequence * lhs, const angbao_navigation2__msg__CustomDetection__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!angbao_navigation2__msg__CustomDetection__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
angbao_navigation2__msg__CustomDetection__Sequence__copy(
  const angbao_navigation2__msg__CustomDetection__Sequence * input,
  angbao_navigation2__msg__CustomDetection__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(angbao_navigation2__msg__CustomDetection);
    angbao_navigation2__msg__CustomDetection * data =
      (angbao_navigation2__msg__CustomDetection *)realloc(output->data, allocation_size);
    if (!data) {
      return false;
    }
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!angbao_navigation2__msg__CustomDetection__init(&data[i])) {
        /* free currently allocated and return false */
        for (; i-- > output->capacity; ) {
          angbao_navigation2__msg__CustomDetection__fini(&data[i]);
        }
        free(data);
        return false;
      }
    }
    output->data = data;
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!angbao_navigation2__msg__CustomDetection__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
