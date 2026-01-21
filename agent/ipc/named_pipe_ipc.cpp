#include "named_pipe_ipc.h"
#include <iostream>

namespace agent_ipc {

    NamedPipeServer::NamedPipeServer(const std::wstring& pipe_name) : pipe_name_(pipe_name) {}
    NamedPipeServer::~NamedPipeServer() { Close(); }

    bool NamedPipeServer::Start() {
        // Sanitize pipe_name_ (must be non-empty, only alnum/_/-)
        std::wstring safe_name;
        for (wchar_t c : pipe_name_) {
            if (iswalnum(c) || c == L'_' || c == L'-') safe_name += c;
        }
        if (safe_name.empty()) safe_name = L"tamsil_agent_pipe";
        std::wstring full = L"\\.\\pipe\\" + safe_name;
        std::wcout << L"[IPC] Creating named pipe: " << full << std::endl;
        pipe_handle_ = CreateNamedPipeW(full.c_str(), PIPE_ACCESS_DUPLEX, PIPE_TYPE_BYTE | PIPE_READMODE_BYTE | PIPE_WAIT,
            PIPE_UNLIMITED_INSTANCES, 4096, 4096, 0, nullptr);
        if (pipe_handle_ == INVALID_HANDLE_VALUE) return false;
        return true;
    }

    bool NamedPipeServer::WaitForClient() {
        if (pipe_handle_ == INVALID_HANDLE_VALUE) return false;
        BOOL connected = ConnectNamedPipe(pipe_handle_, nullptr) ? TRUE : (GetLastError() == ERROR_PIPE_CONNECTED);
        return connected == TRUE;
    }

    bool NamedPipeServer::ReadMessage(std::vector<uint8_t>& out_msg) {
        if (pipe_handle_ == INVALID_HANDLE_VALUE) return false;
        uint32_t size = 0;
        DWORD read = 0;
        if (!ReadFile(pipe_handle_, &size, sizeof(size), &read, nullptr)) return false;
        out_msg.resize(size);
        if (!ReadFile(pipe_handle_, out_msg.data(), size, &read, nullptr)) return false;
        return true;
    }

    bool NamedPipeServer::WriteMessage(const std::vector<uint8_t>& msg) {
        if (pipe_handle_ == INVALID_HANDLE_VALUE) return false;
        DWORD written = 0;
        uint32_t size = (uint32_t)msg.size();
        if (!WriteFile(pipe_handle_, &size, sizeof(size), &written, nullptr)) return false;
        if (!WriteFile(pipe_handle_, msg.data(), size, &written, nullptr)) return false;
        return true;
    }

    void NamedPipeServer::Close() {
        if (pipe_handle_ != INVALID_HANDLE_VALUE) {
            FlushFileBuffers(pipe_handle_);
            DisconnectNamedPipe(pipe_handle_);
            CloseHandle(pipe_handle_);
            pipe_handle_ = INVALID_HANDLE_VALUE;
        }
    }

    NamedPipeClient::NamedPipeClient(const std::wstring& pipe_name) : pipe_name_(pipe_name) {}
    NamedPipeClient::~NamedPipeClient() { Close(); }

    bool NamedPipeClient::Connect() {
        std::wstring full = L"\\.\\pipe\\" + pipe_name_;
        // Wait up to 3s
        DWORD start = GetTickCount();
        while (true) {
            HANDLE h = CreateFileW(full.c_str(), GENERIC_READ | GENERIC_WRITE, 0, nullptr, OPEN_EXISTING, 0, nullptr);
            if (h != INVALID_HANDLE_VALUE) { pipe_handle_ = h; return true; }
            if (GetTickCount() - start > 3000) return false;
            Sleep(50);
        }
    }

    bool NamedPipeClient::ReadMessage(std::vector<uint8_t>& out_msg) {
        if (pipe_handle_ == INVALID_HANDLE_VALUE) return false;
        uint32_t size = 0; DWORD read = 0;
        if (!ReadFile(pipe_handle_, &size, sizeof(size), &read, nullptr)) return false;
        out_msg.resize(size);
        if (!ReadFile(pipe_handle_, out_msg.data(), size, &read, nullptr)) return false;
        return true;
    }

    bool NamedPipeClient::WriteMessage(const std::vector<uint8_t>& msg) {
        if (pipe_handle_ == INVALID_HANDLE_VALUE) return false;
        DWORD written = 0;
        uint32_t size = (uint32_t)msg.size();
        if (!WriteFile(pipe_handle_, &size, sizeof(size), &written, nullptr)) return false;
        if (!WriteFile(pipe_handle_, msg.data(), size, &written, nullptr)) return false;
        return true;
    }

    void NamedPipeClient::Close() {
        if (pipe_handle_ != INVALID_HANDLE_VALUE) {
            CloseHandle(pipe_handle_);
            pipe_handle_ = INVALID_HANDLE_VALUE;
        }
    }

}
