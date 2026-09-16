#!/usr/bin/env python3
"""Batch-export every .blend below this directory to separate glTF files.

Run with a normal Python installation:

    python batch_export_blend_files_to_gltf.py

The script finds Blender on Windows or Linux, including common Steam library
locations, and launches it in background mode once for each .blend file.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable


def _version_key(path: Path) -> tuple[int, ...]:
    numbers = re.findall(r"\d+", str(path.parent))
    return tuple(int(number) for number in numbers[-3:]) if numbers else (0,)


def _steam_roots() -> list[Path]:
    roots: list[Path] = []

    if sys.platform == "win32":
        for variable in ("PROGRAMFILES(X86)", "PROGRAMFILES"):
            if os.environ.get(variable):
                roots.append(Path(os.environ[variable]) / "Steam")

        try:
            import winreg

            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam"
            ) as key:
                roots.append(Path(winreg.QueryValueEx(key, "SteamPath")[0]))
        except (ImportError, FileNotFoundError, OSError):
            pass
    else:
        roots.extend(
            [
                Path.home() / ".steam" / "steam",
                Path.home() / ".local" / "share" / "Steam",
            ]
        )

    libraries: list[Path] = []
    for root in roots:
        if root not in libraries:
            libraries.append(root)

        vdf = root / "steamapps" / "libraryfolders.vdf"
        try:
            text = vdf.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for value in re.findall(r'"path"\s+"([^"]+)"', text):
            library = Path(value.replace("\\\\", "\\"))
            if library not in libraries:
                libraries.append(library)

    return libraries


def find_blender_candidates() -> list[Path]:
    executable = "blender.exe" if sys.platform == "win32" else "blender"
    candidates: list[Path] = []

    for variable in ("BLENDER_EXE", "BLENDER_PATH"):
        if os.environ.get(variable):
            candidates.append(Path(os.environ[variable]).expanduser())

    on_path = shutil.which("blender")
    if on_path:
        candidates.append(Path(on_path))

    if sys.platform == "win32":
        for variable in ("PROGRAMFILES", "PROGRAMFILES(X86)"):
            base = os.environ.get(variable)
            if base:
                candidates.extend(
                    Path(base).glob("Blender Foundation/Blender */blender.exe")
                )
    elif sys.platform.startswith("linux"):
        candidates.extend(Path("/opt").glob("blender*/blender"))
        candidates.extend(
            Path(path)
            for path in (
                "/usr/bin/blender",
                "/usr/local/bin/blender",
                "/snap/bin/blender",
            )
        )

    for steam_root in _steam_roots():
        candidates.append(
            steam_root / "steamapps" / "common" / "Blender" / executable
        )

    unique: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        try:
            candidate = candidate.resolve()
        except OSError:
            continue
        key = os.path.normcase(str(candidate))
        if candidate.is_file() and key not in seen:
            seen.add(key)
            unique.append(candidate)

    # Environment overrides and PATH remain preferred. Discovered installs are
    # ordered newest-first when several Blender versions are installed.
    preferred_count = min(
        sum(bool(os.environ.get(name)) for name in ("BLENDER_EXE", "BLENDER_PATH"))
        + bool(on_path),
        len(unique),
    )
    return unique[:preferred_count] + sorted(
        unique[preferred_count:], key=_version_key, reverse=True
    )


def find_blend_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.blend")
        if "export" not in {part.lower() for part in path.relative_to(root).parts}
    )


def _args_after_double_dash() -> list[str]:
    try:
        return sys.argv[sys.argv.index("--") + 1 :]
    except ValueError:
        return []


def _supported_gltf_properties() -> set[str]:
    import bpy

    try:
        return set(bpy.ops.export_scene.gltf.get_rna_type().properties.keys())
    except Exception:
        return set()


def _set_if_supported(
    options: dict[str, object], supported: set[str], name: str, value: object
) -> None:
    if name in supported:
        options[name] = value


def export_in_blender(output: Path) -> None:
    import bpy

    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    (output.parent / "textures").mkdir(parents=True, exist_ok=True)

    supported = _supported_gltf_properties()
    options: dict[str, object] = {
        "filepath": str(output),
        "export_format": "GLTF_SEPARATE",
    }
    _set_if_supported(options, supported, "export_texture_dir", "textures")
    _set_if_supported(options, supported, "export_apply", True)
    _set_if_supported(options, supported, "export_lights", True)
    _set_if_supported(options, supported, "export_selected", False)
    _set_if_supported(options, supported, "use_selection", False)
    _set_if_supported(options, supported, "export_texcoords", True)
    _set_if_supported(options, supported, "export_normals", True)
    _set_if_supported(options, supported, "export_yup", True)

    result = bpy.ops.export_scene.gltf(**options)
    if "FINISHED" not in result:
        raise RuntimeError(f"glTF export failed: {sorted(result)}")
    print(f"EXPORT_OK: {output}")


def _run_worker() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(_args_after_double_dash())
    export_in_blender(args.output)
    return 0


def _display_command(parts: Iterable[object]) -> str:
    return subprocess.list2cmdline([str(part) for part in parts])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Directory to search recursively (default: directory containing this script)",
    )
    parser.add_argument(
        "--blender",
        type=Path,
        help="Explicit Blender executable; also configurable with BLENDER_EXE",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show exports without launching Blender"
    )
    parser.add_argument(
        "--list-blenders", action="store_true", help="List detected Blender executables"
    )
    args = parser.parse_args()

    candidates = find_blender_candidates()
    if args.list_blenders:
        if args.blender:
            print(args.blender.resolve())
        for candidate in candidates:
            print(candidate)
        return 0

    blender = (
        args.blender.resolve()
        if args.blender
        else (candidates[0] if candidates else None)
    )
    if blender is None or not blender.is_file():
        print(
            "Blender was not found. Pass --blender PATH or set BLENDER_EXE.",
            file=sys.stderr,
        )
        return 2

    root = args.root.resolve()
    blend_files = find_blend_files(root)
    if not blend_files:
        print(f"No .blend files found below {root}")
        return 0

    print(f"Blender: {blender}")
    print(f"Models:  {root}")
    print(f"Found:   {len(blend_files)} .blend file(s)")

    failures: list[Path] = []
    script = Path(__file__).resolve()
    for index, blend_file in enumerate(blend_files, start=1):
        output = blend_file.parent / "export" / f"{blend_file.stem}.gltf"
        command = [
            blender,
            "--background",
            "--factory-startup",
            blend_file,
            "--python",
            script,
            "--",
            "--worker",
            "--output",
            output,
        ]
        print(f"\n[{index}/{len(blend_files)}] {blend_file}")
        print(f"  -> {output}")
        if args.dry_run:
            print(f"  {_display_command(command)}")
            continue

        completed = subprocess.run([str(part) for part in command], check=False)
        if completed.returncode != 0:
            failures.append(blend_file)
            print(f"FAILED ({completed.returncode}): {blend_file}", file=sys.stderr)

    if failures:
        print(f"\n{len(failures)} export(s) failed:", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1

    print(f"\nExported {len(blend_files)} model(s) successfully.")
    return 0


if __name__ == "__main__":
    if "--worker" in _args_after_double_dash():
        raise SystemExit(_run_worker())
    raise SystemExit(main())
