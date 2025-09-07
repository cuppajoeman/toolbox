import os
import sys
import requests


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

    target_dir = os.path.dirname(path)
    target_name = os.path.basename(url)
    target_path = os.path.join(target_dir, target_name)

    print(f"[*] Fetching {url} → {target_path}")

    try:
        r = requests.get(url, stream=True, timeout=30)
        r.raise_for_status()
    except Exception as e:
        print(f"    failed: {e}")
        return

    with open(target_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"    wrote {target_path}")


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
