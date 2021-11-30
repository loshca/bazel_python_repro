import sys
import os
import pathlib
import ctypes

from ctypes import windll, wintypes


def _orig_argv():
    GetCommandLineW = windll.kernel32.GetCommandLineW
    GetCommandLineW.argtypes = []
    GetCommandLineW.restype = wintypes.LPCWSTR

    CommandLineToArgvW = windll.shell32.CommandLineToArgvW
    CommandLineToArgvW.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(ctypes.c_int)]
    CommandLineToArgvW.restype = ctypes.POINTER(wintypes.LPCWSTR)

    LocalFree = windll.kernel32.LocalFree
    LocalFree.argtypes = [wintypes.HLOCAL]
    LocalFree.restype = wintypes.HLOCAL

    cmdline = GetCommandLineW()
    last_error = ctypes.GetLastError()
    if cmdline is None:
        raise ValueError("GetCommandLineW failed: {}", last_error)

    argc = ctypes.c_int()
    argv = CommandLineToArgvW(cmdline, ctypes.byref(argc))
    last_error = ctypes.GetLastError()
    if argv is None:
        raise ValueError("CommandLineToArgvW failed: {}", last_error)

    try:
        result = argv[0 : argc.value]
    finally:
        LocalFree(argv)

    return result


def _setup_path():
    if (sys.version_info.major, sys.version_info.minor) >= (3, 10):
        orig_argv = sys.orig_argv
    else:
        orig_argv = _orig_argv()

    if sys.argv == [""]:
        python_args = orig_argv[1:]
    else:
        python_args = orig_argv[1 : -len(sys.argv)]

    path_0_was_added = False

    # can't check `sys.flags.isolated` because it is always 1 for embedded python, so get flag from command line
    if not "-I" in python_args:
        if sys.argv[0] in ["", "-", "-c"]:
            sys.path.insert(0, "")
        elif sys.argv[0] in ["-m"]:
            sys.path.insert(0, str(pathlib.Path.cwd()))
        else:
            sys.path.insert(0, str(pathlib.Path(sys.argv[0]).absolute().parent))

        path_0_was_added = True

    if not sys.flags.ignore_environment:
        pythonpath = os.environ.get("PYTHONPATH")
        if pythonpath:
            paths_from_pythonpath = pythonpath.split(os.pathsep)
            if path_0_was_added:
                sys.path[1:1] = paths_from_pythonpath
            else:
                sys.path[0:0] = paths_from_pythonpath


_setup_path()
