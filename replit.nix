{pkgs}: {
  deps = [
    pkgs.python312Packages.black
    pkgs.python312Packages.pytest-subtests
    pkgs.python312Packages.pytest
    pkgs.black
    pkgs.ruff
  ];
}
