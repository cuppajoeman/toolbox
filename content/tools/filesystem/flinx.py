#!/usr/bin/env python3
import os
import shutil

FLINX_FILE = ".flinx"

def parse_symlink_file(symlink_file_path):
    mappings = {}
    with open(symlink_file_path, "r") as file:
        for line in file:
            line = line.strip()
            if "->" not in line or line.startswith("#") or not line:
                continue
            src, dst = map(str.strip, line.split("->", 1))
            mappings.setdefault(src, []).append(dst)
    return mappings

def copy_and_clobber(src_path, dst_path):
    """
    Copy src_path to dst_path safely. Overwrites only if types match.
    """
    if os.path.exists(dst_path):
        # Type mismatch
        if os.path.isdir(src_path) and os.path.isfile(dst_path):
            print(f"Warning: Cannot copy directory {src_path} over existing file {dst_path}, skipping.")
            return
        if os.path.isfile(src_path) and os.path.isdir(dst_path):
            print(f"Warning: Cannot copy file {src_path} over existing directory {dst_path}, skipping.")
            return

        print(f"Clobbering existing path: {dst_path}")
        if os.path.isdir(dst_path):
            shutil.rmtree(dst_path)
        else:
            os.remove(dst_path)

    # Ensure parent directories exist
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)

    if os.path.isdir(src_path):
        shutil.copytree(src_path, dst_path)
        print(f"Copied directory {src_path} -> {dst_path}")
    else:
        shutil.copy2(src_path, dst_path)
        print(f"Copied file {src_path} -> {dst_path}")

def main():
    cwd = os.getcwd()
    flinx_file_path = os.path.join(cwd, FLINX_FILE)

    if not os.path.isfile(flinx_file_path):
        print(f"No {FLINX_FILE} file found in current directory, nothing to do.")
        return

    mappings = parse_symlink_file(flinx_file_path)
    base_dir = os.path.dirname(flinx_file_path)

    for subpath, target_paths in mappings.items():
        full_src_path = os.path.join(base_dir, subpath)

        if not os.path.exists(full_src_path):
            print(f"Warning: source path does not exist: {full_src_path}")
            continue

        for target_path in target_paths:
            full_dst_path = os.path.abspath(target_path)
            copy_and_clobber(full_src_path, full_dst_path)

if __name__ == "__main__":
    main()
