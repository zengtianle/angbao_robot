// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from angbao_navigation2:msg/CustomDetection.idl
// generated code does not contain a copyright notice

#ifndef ANGBAO_NAVIGATION2__MSG__DETAIL__CUSTOM_DETECTION__FUNCTIONS_H_
#define ANGBAO_NAVIGATION2__MSG__DETAIL__CUSTOM_DETECTION__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "angbao_navigation2/msg/rosidl_generator_c__visibility_control.h"

#include "angbao_navigation2/msg/detail/custom_detection__struct.h"

/// Initialize msg/CustomDetection message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * angbao_navigation2__msg__CustomDetection
 * )) before or use
 * angbao_navigation2__msg__CustomDetection__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_angbao_navigation2
bool
angbao_navigation2__msg__CustomDetection__init(angbao_navigation2__msg__CustomDetection * msg);

/// Finalize msg/CustomDetection message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_angbao_navigation2
void
angbao_navigation2__msg__CustomDetection__fini(angbao_navigation2__msg__CustomDetection * msg);

/// Create msg/CustomDetection message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * angbao_navigation2__msg__CustomDetection__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_angbao_navigation2
angbao_navigation2__msg__CustomDetection *
angbao_navigation2__msg__CustomDetection__create();

/// Destroy msg/CustomDetection message.
/**
 * It calls
 * angbao_navigation2__msg__CustomDetection__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_angbao_navigation2
void
angbao_navigation2__msg__CustomDetection__destroy(angbao_navigation2__msg__CustomDetection * msg);

/// Check for msg/CustomDetection message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_angbao_navigation2
bool
angbao_navigation2__msg__CustomDetection__are_equal(const angbao_navigation2__msg__CustomDetection * lhs, const angbao_navigation2__msg__CustomDetection * rhs);

/// Copy a msg/CustomDetection message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_angbao_navigation2
bool
angbao_navigation2__msg__CustomDetection__copy(
  const angbao_navigation2__msg__CustomDetection * input,
  angbao_navigation2__msg__CustomDetection * output);

/// Initialize array of msg/CustomDetection messages.
/**
 * It allocates the memory for the number of elements and calls
 * angbao_navigation2__msg__CustomDetection__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_angbao_navigation2
bool
angbao_navigation2__msg__CustomDetection__Sequence__init(angbao_navigation2__msg__CustomDetection__Sequence * array, size_t size);

/// Finalize array of msg/CustomDetection messages.
/**
 * It calls
 * angbao_navigation2__msg__CustomDetection__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_angbao_navigation2
void
angbao_navigation2__msg__CustomDetection__Sequence__fini(angbao_navigation2__msg__CustomDetection__Sequence * array);

/// Create array of msg/CustomDetection messages.
/**
 * It allocates the memory for the array and calls
 * angbao_navigation2__msg__CustomDetection__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_angbao_navigation2
angbao_navigation2__msg__CustomDetection__Sequence *
angbao_navigation2__msg__CustomDetection__Sequence__create(size_t size);

/// Destroy array of msg/CustomDetection messages.
/**
 * It calls
 * angbao_navigation2__msg__CustomDetection__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_angbao_navigation2
void
angbao_navigation2__msg__CustomDetection__Sequence__destroy(angbao_navigation2__msg__CustomDetection__Sequence * array);

/// Check for msg/CustomDetection message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_angbao_navigation2
bool
angbao_navigation2__msg__CustomDetection__Sequence__are_equal(const angbao_navigation2__msg__CustomDetection__Sequence * lhs, const angbao_navigation2__msg__CustomDetection__Sequence * rhs);

/// Copy an array of msg/CustomDetection messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_angbao_navigation2
bool
angbao_navigation2__msg__CustomDetection__Sequence__copy(
  const angbao_navigation2__msg__CustomDetection__Sequence * input,
  angbao_navigation2__msg__CustomDetection__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // ANGBAO_NAVIGATION2__MSG__DETAIL__CUSTOM_DETECTION__FUNCTIONS_H_
