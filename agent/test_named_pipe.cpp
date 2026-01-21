// Minimal named pipe server test
#include <windows.h>
#include <iostream>

int main() {
    const wchar_t* pipe_name = L"\\.\\pipe\\tamsil_agent_pipe";
    std::wcout << L"Creating named pipe: " << pipe_name << std::endl;
    HANDLE pipe = CreateNamedPipeW(
        pipe_name,
        PIPE_ACCESS_DUPLEX,
        PIPE_TYPE_BYTE | PIPE_READMODE_BYTE | PIPE_WAIT,
        PIPE_UNLIMITED_INSTANCES,
        4096, 4096, 0, nullptr);
    if (pipe == INVALID_HANDLE_VALUE) {
        DWORD err = GetLastError();
        std::wcerr << L"Failed to create named pipe. Win32 error: " << err << std::endl;
        return 1;
    }
    std::wcout << L"Named pipe created successfully!" << std::endl;
    CloseHandle(pipe);
    return 0;
}
