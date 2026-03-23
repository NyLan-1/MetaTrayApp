import ctypes
import time
from ctypes import wintypes

user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

WM_CLOSE = 0x0010
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

EnumWindows = user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
GetWindowTextLengthW = user32.GetWindowTextLengthW
GetWindowTextW = user32.GetWindowTextW
IsWindowVisible = user32.IsWindowVisible
GetWindowThreadProcessId = user32.GetWindowThreadProcessId
PostMessageW = user32.PostMessageW

OpenProcess = kernel32.OpenProcess
CloseHandle = kernel32.CloseHandle
QueryFullProcessImageNameW = kernel32.QueryFullProcessImageNameW


def get_window_text(hwnd: int) -> str:
    length = GetWindowTextLengthW(hwnd)
    if length == 0:
        return ""
    buffer = ctypes.create_unicode_buffer(length + 1)
    GetWindowTextW(hwnd, buffer, length + 1)
    return buffer.value.strip()


def get_process_name(pid: int) -> str:
    hprocess = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not hprocess:
        return ""

    try:
        size = wintypes.DWORD(260)
        buffer = ctypes.create_unicode_buffer(size.value)
        if QueryFullProcessImageNameW(hprocess, 0, buffer, ctypes.byref(size)):
            return buffer.value.split("\\")[-1].lower()
        return ""
    finally:
        CloseHandle(hprocess)


def find_meta_window():
    matches = []

    def enum_callback(hwnd, lparam):
        if not IsWindowVisible(hwnd):
            return True

        title = get_window_text(hwnd)
        if not title:
            return True

        pid = wintypes.DWORD()
        GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        process_name = get_process_name(pid.value)

        if process_name in {"chrome.exe", "msedge.exe", "firefox.exe"}:
            return True

        title_l = title.lower()
        proc_l = process_name.lower()

        if (
            "oculus" in proc_l
            or "meta" in proc_l
            or "horizon link" in title_l
            or "meta horizon link" in title_l
            or "meta quest link" in title_l
        ):
            matches.append((hwnd, process_name, title))

        return True

    EnumWindows(EnumWindowsProc(enum_callback), 0)
    return matches[0] if matches else None


def main():
    timeout_seconds = 30
    deadline = time.time() + timeout_seconds
    already_closed = set()

    while time.time() < deadline:
        result = find_meta_window()
        if result:
            hwnd, process_name, title = result

            if hwnd not in already_closed:
                PostMessageW(hwnd, WM_CLOSE, 0, 0)
                already_closed.add(hwnd)

                time.sleep(1)

                result_after = find_meta_window()
                if not result_after:
                    return

        time.sleep(0.3)


if __name__ == "__main__":
    main()