#!/bin/bash

# Function to display help message
show_help() {
    echo "Usage: $0 -l <local_dir> -r <remote_user>@<remote_host>:<remote_dir>"
    echo ""
    echo "Options:"
    echo "  -l, --local      Local directory to monitor"
    echo "  -r, --remote     Remote user, host, and directory in the format user@host:/path/to/dir"
    echo "  -h, --help       Show this help message"
    exit 1
}

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -l|--local)
            LOCAL_DIR="$2"
            shift 2
            ;;
        -r|--remote)
            REMOTE_INFO="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            ;;
        *)
            echo "Unknown parameter passed: $1"
            show_help
            ;;
    esac
done

# Check if required arguments are provided
if [ -z "$LOCAL_DIR" ] || [ -z "$REMOTE_INFO" ]; then
    echo "Error: Missing required arguments."
    show_help
fi

# Parse remote information
REMOTE_USER=$(echo "$REMOTE_INFO" | cut -d'@' -f1)
REMOTE_HOST=$(echo "$REMOTE_INFO" | cut -d'@' -f2 | cut -d':' -f1)
REMOTE_DIR=$(echo "$REMOTE_INFO" | cut -d':' -f2)

# Ensure inotifywait is installed
if ! command -v inotifywait &> /dev/null; then
    echo "inotifywait could not be found. Please install inotify-tools."
    exit 1
fi

# Ensure rsync is installed
if ! command -v rsync &> /dev/null; then
    echo "rsync could not be found. Please install rsync."
    exit 1
fi

echo "Monitoring directory: $LOCAL_DIR"
echo "Syncing to $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR"

# Function to sync changes
sync_files() {
    # rsync command explanation:
    # -a : archive mode, preserves permissions, symlinks, etc.
    # -v : verbose mode, shows detailed output
    # -z : compresses data during the transfer for faster sync
    # --delete : deletes files in the remote directory if they were deleted in the local directory
    # "$LOCAL_DIR/" : source directory, trailing slash ensures contents of the directory are copied
    # "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR" : destination on the remote server
    rsync -avz --delete "$LOCAL_DIR/" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR"
}

# Initial sync to ensure both directories are in sync
sync_files

# Monitor the directory for changes and sync when they occur
inotifywait -m -r -e modify,create,delete,move "$LOCAL_DIR" --format '%w%f' | while read change; do
    echo "Detected change: $change"
    sync_files
    echo "Sync complete."
done
