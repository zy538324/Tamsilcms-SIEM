add_executable(agent_execution
    main.cpp
    service_entry.cpp
    ExecutionService_stub.cpp
    RegisterService_stub.cpp
    ../agent_config.cpp
    ../agent_patch_jobs.cpp
    ../agent_rmm.cpp
    ../agent_signing.cpp
    ../core/uplink.cpp
)

target_include_directories(agent_execution PRIVATE ../../include)

target_link_libraries(agent_execution PRIVATE agent_ipc ${AGENT_LIBS} advapi32)
