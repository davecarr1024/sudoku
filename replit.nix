{pkgs}: {
  deps = [
    pkgs.python312Packages.matplotlib
    pkgs.python312Packages.numpy
    pkgs.python311Packages.memory-profiler
    pkgs.python312Packages.memory-profiler
    pkgs.python312Packages.mypy
    pkgs.python312Packages.black
    pkgs.python312Packages.pytest-subtests
    pkgs.python312Packages.pytest
    pkgs.black
    pkgs.ruff
  ];
}
