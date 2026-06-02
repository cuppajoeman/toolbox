import os
import re
import unicodedata

MUSIC_DIR = "."


def simplify_filename(name: str) -> str:
    base, ext = os.path.splitext(name)

    # Normalize unicode (handles weird characters like ：)
    base = unicodedata.normalize("NFKD", base).encode("ascii", "ignore").decode()

    # Remove bracketed metadata like [v3gOQbh32Pg], [Audio], etc.
    base = re.sub(r"\[[^\]]*\]", "", base)

    # Replace spaces, hyphens, and dots with underscores
    base = base.replace(" ", "_").replace("-", "_").replace(".", "_")

    # Remove unwanted characters (keep alnum and underscore)
    base = re.sub(r"[^A-Za-z0-9_]", "", base)

    # Collapse multiple underscores into one
    base = re.sub(r"_+", "_", base)

    # Strip leading/trailing underscores
    base = base.strip("_")

    return base.lower() + ext.lower()


def main():
    for filename in os.listdir(MUSIC_DIR):
        old_path = os.path.join(MUSIC_DIR, filename)

        if not os.path.isfile(old_path):
            continue

        if not filename.lower().endswith(".mp3"):
            continue

        new_name = simplify_filename(filename)

        if new_name != filename:
            new_path = os.path.join(MUSIC_DIR, new_name)
            print(f"{filename} -> {new_name}")
            os.rename(old_path, new_path)


if __name__ == "__main__":
    main()
