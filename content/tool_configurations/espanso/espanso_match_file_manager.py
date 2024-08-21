#!/usr/bin/env python3

import os
import argparse

# Get the espanso configuration path
def get_espanso_config_path():
    result = os.popen("espanso path config").read().strip()
    return result

# Append .yml extension if missing
def ensure_yml_extension(filename):
    if not filename.endswith(".yml"):
        filename += ".yml"
    return filename

# List all .yml files, active and disabled
def list_files(match_dir):
    active_files = []
    disabled_files = []

    for file in os.listdir(match_dir):
        if file.endswith(".yml"):
            if file.startswith("_"):
                disabled_files.append(file)
            else:
                active_files.append(file)

    print("Active match files:")
    for file in active_files:
        print(f"  {file}")

    print("\nDisabled match files:")
    for file in disabled_files:
        print(f"  {file}")

# Enable a specific match file
def enable_file(match_dir, filename):
    filename = ensure_yml_extension(filename)
    disabled_filename = f"_{filename}"
    
    if os.path.exists(os.path.join(match_dir, disabled_filename)):
        src = os.path.join(match_dir, disabled_filename)
        dst = os.path.join(match_dir, filename)
        os.rename(src, dst)
        print(f"Enabled: {dst}")
    else:
        print(f"{filename} is already enabled or does not exist.")

# Disable a specific match file
def disable_file(match_dir, filename):
    filename = ensure_yml_extension(filename)
    if not filename.startswith("_"):
        src = os.path.join(match_dir, filename)
        dst = os.path.join(match_dir, f"_{filename}")
        if os.path.exists(src):
            os.rename(src, dst)
            print(f"Disabled: {dst}")
        else:
            print(f"{filename} does not exist.")
    else:
        print(f"{filename} is already disabled.")

# Process a config file to enable or disable files
def process_config_file(match_dir, config_file):
    with open(config_file, 'r') as file:
        config_files = file.read().splitlines()

    all_files = {f.lstrip("_").rstrip(".yml"): f for f in os.listdir(match_dir) if f.endswith(".yml")}

    # Disable all match files
    for file in all_files.values():
        if not file.startswith("_"):
            disable_file(match_dir, file.rstrip(".yml"))

    # Enable the ones specified in config
    for config in config_files:
        if config in all_files:
            enable_file(match_dir, config)
        else:
            print(f"Warning: {config}.yml not found in match directory.")

# Main function
def main():
    parser = argparse.ArgumentParser(description="Manage espanso match files.")
    subparsers = parser.add_subparsers(dest='command', help="Subcommands")

    # List subcommand
    list_parser = subparsers.add_parser('list', help='List all match files (active and disabled).')

    # Enable subcommand
    enable_parser = subparsers.add_parser(
        'enable', 
        help='Enable a match file by filename (without or with .yml extension).'
    )
    enable_parser.add_argument('file', metavar='FILE', type=str, help='The match file to enable (without .yml extension).')

    # Disable subcommand
    disable_parser = subparsers.add_parser(
        'disable', 
        help='Disable a match file by filename (without or with .yml extension).'
    )
    disable_parser.add_argument('file', metavar='FILE', type=str, help='The match file to disable (without .yml extension).')

    # Config subcommand with RawTextHelpFormatter to preserve formatting
    config_parser = subparsers.add_parser(
        'config',
        help='Specify a config file to enable/disable match files.',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""\
Config File Format:
-------------------
A valid config file is a plain text file where each line contains the name of a match file (without the .yml extension) that you want to activate. All other match files will be disabled. The file should not contain any extra spaces or characters other than the match file names.

Example:
--------
file1
file2

This will activate 'file1.yml' and 'file2.yml', while disabling all other '.yml' files in the 'match' directory.
"""
    )
    config_parser.add_argument('config', metavar='CONFIG', type=str, help='Path to the config file.')

    args = parser.parse_args()

    espanso_config_path = get_espanso_config_path()
    match_dir = os.path.join(espanso_config_path, 'match')

    if args.command == 'list':
        list_files(match_dir)
    elif args.command == 'enable':
        enable_file(match_dir, args.file)
    elif args.command == 'disable':
        disable_file(match_dir, args.file)
    elif args.command == 'config':
        process_config_file(match_dir, args.config)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
