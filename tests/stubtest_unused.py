#!/usr/bin/env python3

# Runs stubtest and prints each unused allowlist entry with filename.
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

_UNUSED_NOTE = "note: unused allowlist entry "
_ALLOWLIST_PATH = Path("tests") / "stubtest_allowlists"


def main() -> None:
    unused = run_stubtest()
    with_filenames = []
    for uu in unused:
        with_filenames.extend(unused_files(uu))
    for file, uu in with_filenames:
        print(f"{file}:{uu}")


def run_stubtest() -> List[str]:
    proc = subprocess.run([sys.executable, "tests/stubtest_stdlib.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = proc.stdout.decode("utf-8").splitlines()
    return [line[len(_UNUSED_NOTE) :].strip() for line in output if line.startswith(_UNUSED_NOTE)]


def unused_files(unused: str) -> List[Tuple[str, str]]:
    version = f"py{sys.version_info[0]}{sys.version_info[1]}"
    files = [
        "py3_common.txt",
        f"{version}.txt",
        f"{sys.platform}.txt",
        f"{sys.platform}-{version}.txt",
    ]

    found = []
    for file in files:
        path = _ALLOWLIST_PATH / file
        if find_unused_in_file(unused, path):
            found.append((path.as_posix(), unused))
    if not found:
        raise ValueError(f"unused item {unused} not found in any allowlist file")
    return found


def find_unused_in_file(unused: str, path: Path) -> bool:
    try:
        with open(path) as f:
            return any(line.strip().split(" ")[0] == unused for line in f)
    except FileNotFoundError:
        return False


if __name__ == "__main__":
    main()
