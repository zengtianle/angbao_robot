# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_depointcloud_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED depointcloud_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(depointcloud_FOUND FALSE)
  elseif(NOT depointcloud_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(depointcloud_FOUND FALSE)
  endif()
  return()
endif()
set(_depointcloud_CONFIG_INCLUDED TRUE)

# output package information
if(NOT depointcloud_FIND_QUIETLY)
  message(STATUS "Found depointcloud: 0.0.0 (${depointcloud_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'depointcloud' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT ${depointcloud_DEPRECATED_QUIET})
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(depointcloud_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${depointcloud_DIR}/${_extra}")
endforeach()
