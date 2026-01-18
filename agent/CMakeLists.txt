cmake_minimum_required(VERSION 3.20)
project(agent_hello LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(OpenSSL REQUIRED)
find_package(CURL REQUIRED)

add_executable(agent_hello
    src/main.cpp
    src/agent_config.cpp
    src/agent_crash.cpp
    src/agent_id.cpp
    src/agent_signing.cpp
    src/agent_heartbeat.cpp
    src/agent_integrity.cpp
    src/agent_retry.cpp
    src/agent_system.cpp
    src/agent_uptime.cpp
    src/agent_watchdog.cpp
)

target_include_directories(agent_hello PRIVATE include)

target_link_libraries(agent_hello PRIVATE OpenSSL::SSL OpenSSL::Crypto CURL::libcurl)
