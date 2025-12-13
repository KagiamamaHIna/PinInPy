cmake_minimum_required(VERSION 3.15)
project(PinInPy LANGUAGES C CXX)

if(MSVC)
    add_compile_options(/utf-8)
endif()

set(PININ4CPP_INSTALL OFF CACHE INTERNAL "")
add_subdirectory("PinIn4Cpp")

find_package(Python3 COMPONENTS Interpreter Development.Module REQUIRED)

set(PY_BINDING_DIR "${CMAKE_CURRENT_SOURCE_DIR}")

# 生成 CFFI 胶水代码 (.c)
set(GENERATED_C "${CMAKE_CURRENT_BINARY_DIR}/_pinin4cpp_cffi.c")

add_custom_command(
    OUTPUT ${GENERATED_C}
    COMMAND "${Python3_EXECUTABLE}" "${PY_BINDING_DIR}/build_cffi.py"
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    DEPENDS "${PY_BINDING_DIR}/build_cffi.py"
)

# Python编译模块
python3_add_library(_pinin4cpp_cffi MODULE ${GENERATED_C})

target_link_libraries(_pinin4cpp_cffi PRIVATE PinIn4Cpp::PinIn4Cpp)
target_link_libraries(_pinin4cpp_cffi PRIVATE Python3::Module)

install(TARGETS _pinin4cpp_cffi DESTINATION PinInPy)
install(FILES PinIn4Cpp/LICENSE DESTINATION PinInPy/PinIn4Cpp)
install(DIRECTORY PinIn4Cpp/licenses/ DESTINATION PinInPy/PinIn4Cpp/licenses)
install(DIRECTORY package/ DESTINATION PinInPy)
