#!/usr/bin/env python3

import argparse
import os
import math
import sys


def parse_size(size_str: str) -> int:
    size_str = size_str.strip().upper()

    if size_str.endswith("K"):
        return int(size_str[:-1]) * 1024
    if size_str.endswith("M"):
        return int(size_str[:-1]) * 1024 * 1024
    if size_str.endswith("G"):
        return int(size_str[:-1]) * 1024 * 1024 * 1024

    return int(size_str)


def write_meta(
    meta_path: str, original_name: str, part_size: int, total_parts: int
) -> None:
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write(f"original_name={original_name}\n")
        f.write(f"part_size={part_size}\n")
        f.write(f"total_parts={total_parts}\n")


def read_meta(meta_path: str) -> dict:
    meta = {}
    with open(meta_path, "r", encoding="utf-8") as f:
        for line in f:
            key, value = line.strip().split("=", 1)
            meta[key] = value
    return meta


def split_file(file_path: str, part_size: int) -> None:
    if not os.path.isfile(file_path):
        sys.exit(f"Not a file: {file_path}")

    file_size = os.path.getsize(file_path)
    total_parts = math.ceil(file_size / part_size)

    output_dir = os.path.basename(file_path) + ".parts"

    if os.path.exists(output_dir):
        sys.exit(f"Output directory already exists: {output_dir}")

    os.makedirs(output_dir)

    with open(file_path, "rb") as src:
        for part_index in range(total_parts):
            part_path = os.path.join(output_dir, f"part_{part_index:04d}")
            with open(part_path, "wb") as dst:
                dst.write(src.read(part_size))

    write_meta(
        os.path.join(output_dir, "meta.txt"),
        os.path.basename(file_path),
        part_size,
        total_parts,
    )

    print(f"Split '{file_path}' into {total_parts} parts → '{output_dir}/'")


def join_file(input_dir: str) -> None:
    if not os.path.isdir(input_dir):
        sys.exit(f"Not a directory: {input_dir}")

    meta_path = os.path.join(input_dir, "meta.txt")
    if not os.path.exists(meta_path):
        sys.exit("meta.txt not found")

    meta = read_meta(meta_path)

    output_name = meta["original_name"]
    total_parts = int(meta["total_parts"])

    with open(output_name, "wb") as out:
        for part_index in range(total_parts):
            part_path = os.path.join(input_dir, f"part_{part_index:04d}")
            if not os.path.exists(part_path):
                sys.exit(f"Missing part: {part_path}")

            with open(part_path, "rb") as part:
                out.write(part.read())

    print(f"Reconstructed file '{output_name}'")


def main():
    parser = argparse.ArgumentParser(
        description="Split files into fixed-size chunks and reassemble them"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    split_parser = subparsers.add_parser("split", help="Split a file into parts")
    split_parser.add_argument("file", help="File to split")
    split_parser.add_argument("--size", default="50M", help="Chunk size (default: 50M)")

    join_parser = subparsers.add_parser("join", help="Reassemble a file")
    join_parser.add_argument("directory", help="Directory containing file parts")

    args = parser.parse_args()

    if args.command == "split":
        split_file(args.file, parse_size(args.size))
    elif args.command == "join":
        join_file(args.directory)


if __name__ == "__main__":
    main()
