#!/bin/bash

# Check if pdfgrep is installed
if ! command -v pdfgrep &> /dev/null
then
    echo "pdfgrep could not be found. Please install it before running this script."
    exit 1
fi

# Check if a pattern and path were provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 'pattern' /path/to/search"
    exit 1
fi

# Assign arguments to variables
pattern="$1"
search_path="$2"

# Run pdfgrep with the provided pattern and path
pdfgrep -R "$pattern" "$search_path"

# Check if the command was successful
# if [ $? -eq 0 ]; then
#     echo -e "\e[92mSearch completed successfully.\e[0m" # Bright green success message
# else
#     echo "Search failed or no matches were found."
# fi
