cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)

project(testPing C CXX ASM)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

pico_sdk_init()

add_executable(testPing 
	testPing.cpp
)

pico_enable_stdio_usb(testPing 1)
pico_enable_stdio_uart(testPing 1)

pico_add_extra_outputs(testPing)



add_subdirectory(/home/auke/Documents/_git/school/project56/pico/pico-arduino-compat/libs/ping-arduino build-pac-ping-arduino)


find_library(Softwareserial)
target_link_libraries(testPing pico_stdlib)
target_link_libraries(testPing pac-ping-arduino)
