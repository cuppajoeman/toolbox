import os
import sys
import shutil
import requests


def fetch_url_to_file(url, target_path):
    """Download a URL to a file."""
    print(f"[*] Fetching {url} → {target_path}")
    try:
        r = requests.get(url, stream=True, timeout=30)
        r.raise_for_status()
    except Exception as e:
        print(f"    failed: {e}")
        return False

    with open(target_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"    wrote {target_path}")
    return True


def copy_local_file(src_path, target_path):
    """Copy a local file to the target path."""
    print(f"[*] Copying {src_path} → {target_path}")

    if not os.path.exists(src_path):
        print(f"    failed: source does not exist")
        return False

    try:
        shutil.copy2(src_path, target_path)
    except Exception as e:
        print(f"    failed: {e}")
        return False

    print(f"    wrote {target_path}")
    return True


def process_ifile(path):
    url = None
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("URL="):
                url = line.split("=", 1)[1]

    if not url:
        print(f"[!] {path}: missing URL")
        return

    url = url.strip()

    target_dir = os.path.dirname(path)

    # Determine target filename
    if url.startswith(("http://", "https://")):
        target_name = os.path.basename(url)
    else:
        expanded = os.path.expanduser(url)
        target_name = os.path.basename(expanded)

    target_path = os.path.join(target_dir, target_name)

    # Handle URL vs local file
    if url.startswith(("http://", "https://")):
        fetch_url_to_file(url, target_path)
    else:
        # treat as local file path
        src_path = os.path.expanduser(url)
        src_path = os.path.abspath(src_path)
        copy_local_file(src_path, target_path)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: python indirect_files.py <directory>")
        sys.exit(1)

    root_dir = sys.argv[1]
    if not os.path.isdir(root_dir):
        print(f"[!] Not a directory: {root_dir}")
        sys.exit(1)

    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.endswith(".ifile"):
                process_ifile(os.path.join(dirpath, fname))


if __name__ == "__main__":
    main()
