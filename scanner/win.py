import ctypes

# https://sudonull.com/post/145181-Python-threading-or-GIL-is-almost-no-hindrance
__setaffinity = ctypes.windll.kernel32.SetProcessAffinityMask
__setaffinity.argtypes = [ctypes.c_uint, ctypes.c_uint]

def __open_process(pid, ro=True):
    if not pid:
        pid = os.getpid()
    access = PROCESS_QUERY_INFORMATION
    if not ro:
        access |= PROCESS_SET_INFORMATION
    hProc = ctypes.windll.kernel32.OpenProcess(access, 0, pid)
    if not hProc:
        raise OSError
    return hProc

def set_affinity(pid=0, mask=1):
    hProc = __open_process(pid, ro=False)
    mask_proc = ctypes.c_uint(mask)
    res = __setaffinity(hProc, mask_proc)
    __close_handle(hProc)
    if not res:
        raise OSError
    return