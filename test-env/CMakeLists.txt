cmake_minimum_required(VERSION 3.10)

project(test-env)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")

set(Boost_USE_STATIC_LIBS ON)
find_package(Boost REQUIRED COMPONENTS asio beast thread serialization archive)
include_directories(${Boost_INCLUDE_DIRS})

find_package(CURL REQUIRED)
include_directories(${CURL_INCLUDE_DIRS})

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/libs/nlohmann)

add_executable(test-env src/main.cpp)

# Link libraries
target_link_libraries(test-env PRIVATE ${CURL_LIBRARIES})
target_link_libraries(test-env PRIVATE curl)
target_link_libraries(test-env PRIVATE boost_thread boost_system boost_serialization)

