#!/bin/sh

# Directory where the script is run
dir="$(pwd)"

# Output file
output="$HOME/.vimrc"

# List of files to include (edit this list if needed)
files="
leader.vim
tabs.vim
help.vim
easy_file_opening.vim
easy_editing.vim
easy_window_navigation.vim
go_back_to_where_you_left_off.vim
split_settings.vim
search_settings.vim
visual_info.vim
folds.vim
buffers.vim
fuzzy_file_opening.vim
resizing_windows.vim
file_browser.vim
"

# If ~/.vimrc already exists, ask before overwriting
if [ -f "$output" ]; then
    echo "$output already exists."
    printf "Do you want to overwrite it? (y/N): "
    read ans
    case "$ans" in
        [yY]|[yY][eE][sS]) echo "Overwriting...";;
        *) echo "Aborted."; exit 1;;
    esac
fi

# Write header
echo "\" Auto-generated vimrc" > "$output"
echo "\" Generated on $(date)" >> "$output"
echo >> "$output"

# Write sources for the selected files
for f in $files; do
    if [ -f "$dir/$f" ]; then
        echo "source $dir/$f" >> "$output"
    else
        echo "\" Skipped missing file: $dir/$f" >> "$output"
    fi
done

echo "Generated $output with sources to selected .vim files"
