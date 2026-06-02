#!/bin/bash

# Check if a program name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <program_name>"
  exit 1
fi

program_name=$1

# Check if fzf is installed
if ! command -v fzf &> /dev/null; then
  echo "fzf could not be found. Please install it first."
  exit 1
fi

# Use fzf to select a file recursively from the current directory and open it with the provided program
file=$(find . -type f | fzf)

if [ -n "$file" ]; then
  $program_name "$file"
else
  echo "No file selected."
  exit 1
fi
