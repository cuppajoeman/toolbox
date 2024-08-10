#!/bin/bash

# Script Documentation
print_help() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS]

This script allows you to select a directory from a predefined list of common
paths and change to that directory. You can also add the current directory to
the list of common paths.

Options:
  -h, --help    Show this help message and exit
  -a, --add     Add the current directory to the common paths file

Example:
  $(basename "$0")
  $(basename "$0") -a

EOF
}

# Determine the directory of the script
script_dir="$(dirname "$(realpath "$0")")"
common_paths_file="$script_dir/common_paths.txt"

# Check if fzf is installed
if ! command -v fzf &> /dev/null; then
    echo "fzf is not available on this system, please install it first"
    exit 1
fi

# Parse command-line options
add_current_dir=false

while [[ "$1" =~ ^- ]]; do
    case "$1" in
        -h|--help)
            print_help
            exit 0
            ;;
        -a|--add)
            add_current_dir=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            print_help
            exit 1
            ;;
    esac
done

# Add the current directory to the common paths file if requested
if $add_current_dir; then
    current_dir=$(pwd)
    if grep -q "^$current_dir$" "$common_paths_file"; then
        echo "The current directory is already in the common paths list."
    else
        echo "$current_dir" >> "$common_paths_file"
        echo "Added the current directory to the common paths list."
    fi
    exit 0
fi

# Check if the common paths file exists
if [[ ! -f "$common_paths_file" ]]; then
    echo "Error: The file '$common_paths_file' does not exist."
    exit 1
fi

# Use fzf to select a directory from the file
selected_path=$(cat "$common_paths_file" | fzf --prompt="Select a directory: ")

if [[ -z "$selected_path" ]]; then
    echo "No directory selected, exiting..."
    exit 1
fi

# Expand the ~ symbol in the selected path and change to the directory
expanded_path=$(eval echo "$selected_path")
echo "Changing directory to: $expanded_path"
cd "$expanded_path" || exit

# Optionally, you might want to open a shell in the selected directory
exec bash
