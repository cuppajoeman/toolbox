import os
import json

music_dir = "."

output_file = "playlist.json"

tracks = []
for root, dirs, files in os.walk(music_dir):
    for f in files:
        if f.lower().endswith(".mp3"):
            # Make the path relative to this script, without ./ at start
            rel_path = os.path.join(root, f).replace("\\", "/")
            if rel_path.startswith("./"):
                rel_path = rel_path[2:]
            tracks.append(rel_path)

tracks.sort()

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(tracks, f, indent=2)

print(f"Generated {output_file} with {len(tracks)} tracks.")
