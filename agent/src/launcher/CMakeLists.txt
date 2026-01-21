add_executable(tamsilcms
    main.cpp
)

target_include_directories(tamsilcms PRIVATE ../../include)

target_link_libraries(tamsilcms PRIVATE advapi32)
