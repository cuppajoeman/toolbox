import os

# GitHub single file limit in bytes (100 MB)
GIT_FILE_LIMIT = 100 * 1024 * 1024

# Directory to scan
ROOT_DIR = "."


def bytes_to_readable(size):
    """Convert bytes to a human-readable string."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"


def main():
    print(
        f"Scanning '{ROOT_DIR}' for files over {bytes_to_readable(GIT_FILE_LIMIT)}...\n"
    )
    found = False
    for dirpath, _, filenames in os.walk(ROOT_DIR):
        for fname in filenames:
            path = os.path.join(dirpath, fname)
            try:
                size = os.path.getsize(path)
            except OSError:
                continue
            if size > GIT_FILE_LIMIT:
                print(f"{path} — {bytes_to_readable(size)}")
                found = True
    if not found:
        print("No files exceed the GitHub 100 MB limit.")


if __name__ == "__main__":
    main()
