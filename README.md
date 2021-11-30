# bazel_python_repro

Rule with py_binary, which fails with "LAUNCHER ERROR: Cannot launch process: "python.exe" C:\Users\vasilchuk\_bazel_vasilchuk\odrccifu\execroot\__main__\bazel-out\host\bin\tool.zip"
```
bazel build :generate_smth -s --verbose_failures --experimental_use_windows_sandbox --spawn_strategy=sandboxed --experimental_windows_sandbox_path=... --toolchain_resolution_debug --genrule_strategy=sandboxed    
```


genrule which works:
```
bazel build :generate_smth2 -s --verbose_failures --experimental_use_windows_sandbox --spawn_strategy=sandboxed --experimental_windows_sandbox_path=... --toolchain_resolution_debug --genrule_strategy=sandboxed    
```

If disable sandbox both rules works.




