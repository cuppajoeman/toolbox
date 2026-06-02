#!/bin/bash

# Script Documentation
print_help() {
    cat << EOF
Usage: $(basename "$0") [OPTIONS]

This script opens fzf in the current directory, allowing you to select a file, 
and then opens the selected file in vim.

Options:
  -h, --help    Show this help message and exit

Example:
  $(basename "$0")

EOF
}

# Parse command-line options
while [[ "$1" =~ ^- ]]; do
    case "$1" in
        -h|--help)
            print_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            print_help
            exit 1
            ;;
    esac
done

# Check if fzf is installed
if ! command -v fzf &> /dev/null; then
    echo "fzf is not available on this system, please install it first"
    exit 1
fi

# Select a file using fzf
selected_file=$(find "$(pwd)" -type f | fzf)

# Check if a file was selected
if [[ -z "$selected_file" ]]; then
    echo "No file selected, exiting..."
    exit 1
fi

# Open the selected file in vim
vim "$selected_file"
