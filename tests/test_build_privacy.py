#!/usr/bin/env python3
"""Exercise real compiler path mapping and binary path detection."""
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_privacy import PREBUILT_SDK_PATHS, compiler_flags, find_local_paths, path_spellings


class BuildPrivacyTests(unittest.TestCase):
    def test_paths_in_utf8_and_utf16_are_detected(self):
        samples = [
            "E:/Users/Example/Downloads/project/source.cpp",
            r"e:\Users\Example\Downloads\project\source.cpp",
            "/e/Users/Example/Downloads/project/source.cpp",
            "/mnt/c/Users/Example/project/source.cpp",
            "/cygdrive/c/Users/Example/project/source.cpp",
            "/home/example/project/source.cpp",
            "/Users/Example/project/source.cpp",
            "/workspace/example/project/source.cpp",
            "/tmp/example/source.cpp",
            r"\\computer\share\source.cpp",
            "/custom-location/private-project/source.cpp",
        ]
        for sample in samples:
            for encoding in ("utf-8", "utf-16-le", "utf-16-be"):
                with self.subTest(sample=sample, encoding=encoding):
                    data = b"\x00\x01\x02" + sample.encode(encoding) + b"\x00\x00"
                    self.assertTrue(find_local_paths(data, ["/custom-location/private-project"]))

    def test_runtime_relative_and_neutral_paths_are_allowed(self):
        data = (b"sdmc:/switch/IsaacHUD/catalog_it.tsv\0"
                b"./switch_build/libs/libtesla/include/stb_truetype.h\0"
                b"/opt/devkitpro/libnx/include/switch.h\0"
                b"/build-home/include/header.hpp\0"
                b"https://github.com/NullByteNX/IsaacHUD-Switch\0")
        self.assertFalse(find_local_paths(data, ["/private-project"]))

    def test_msys_and_native_paths_are_both_mapped(self):
        def cygpath(arguments, **kwargs):
            value = "E:/Users/Example/project" if arguments[1] == "-m" else "/e/Users/Example/project"
            return subprocess.CompletedProcess(arguments, 0, value + "\n")
        with patch("build_privacy.shutil.which", return_value="cygpath"), \
                patch("build_privacy.subprocess.run", side_effect=cygpath):
            self.assertEqual(path_spellings("/e/Users/Example/project"),
                             {"/e/Users/Example/project", "E:/Users/Example/project"})

    def test_external_sdk_paths_are_allowed_but_never_current_machine_paths(self):
        for root in PREBUILT_SDK_PATHS:
            for encoding in ("utf-8", "utf-16-le", "utf-16-be"):
                with self.subTest(root=root, encoding=encoding):
                    data = b"\x00\x01\x02" + (root + "src/library.c").encode(encoding) + b"\x00\x00"
                    self.assertFalse(find_local_paths(data, ["/home/overlay-author"]))
                    # An SDK exception must not override the actual build home.
                    self.assertTrue(find_local_paths(data, ["/home/davem"]))
                    for private in ("/home/overlay-author/project/main.cpp",
                                    "E:/Users/Example/project/main.cpp"):
                        mixed = data + private.encode(encoding) + b"\x00\x00"
                        self.assertTrue(find_local_paths(mixed, ["/home/overlay-author"]))
        for path in ("/home/davem/private-project/main.cpp",
                     "/home/another/projects/devkitpro/pacman-packages/libnx/src/file.c",
                     PREBUILT_SDK_PATHS[0].rstrip("/") + "-private/main.cpp"):
            self.assertTrue(find_local_paths(path.encode(), []))

    def test_compiled_object_and_executable_do_not_contain_build_paths(self):
        compiler = shutil.which("g++")
        self.assertIsNotNone(compiler, "g++ is required by make host-test")
        with tempfile.TemporaryDirectory(prefix="isaac privacy ") as directory:
            home = Path(directory) / "Example Person"
            project = home / "project"
            project.mkdir(parents=True)
            source = project / "paths.cpp"
            source.write_text(
                '#include <cstdio>\n'
                'int main() { std::puts(__FILE__); std::puts(__BASE_FILE__); '
                'std::puts(__builtin_FILE()); }\n', encoding="utf-8")
            flags = compiler_flags(project=project, home=home, devkit="/neutral-sdk")
            # The shell form used by Make must preserve spaces in prefixes.
            self.assertEqual(shlex.split(shlex.join(flags)), flags)
            original = project / "original.o"
            sanitized = project / "mapped.o"
            executable = project / "mapped.exe"
            common = [compiler, "-g", "-O0", "-std=c++20"]
            subprocess.run(common + ["-c", str(source), "-o", str(original)],
                           cwd=project, check=True)
            self.assertTrue(find_local_paths(original.read_bytes(), [str(home)]))
            subprocess.run(common + flags + ["-c", str(source), "-o", str(sanitized)],
                           cwd=project, check=True)
            self.assertFalse(find_local_paths(sanitized.read_bytes(), [str(home)]))
            subprocess.run([compiler, str(sanitized), "-o", str(executable)],
                           cwd=project, check=True)
            self.assertFalse(find_local_paths(executable.read_bytes(), [str(home)]))
            output = subprocess.run([str(executable)], capture_output=True,
                                    text=True, check=True).stdout.splitlines()
            self.assertEqual(output, ["./paths.cpp"] * 3)


if __name__ == "__main__":
    unittest.main()
