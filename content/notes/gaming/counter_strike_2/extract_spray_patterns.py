import base64
import json
import re
import urllib.request
from pathlib import Path


HERE = Path(__file__.replace("\\", "/")).resolve().parent
OUTPUT_PATH = HERE / "spray_patterns.json"
SOURCE_URL = "https://op.gg/cs2/spray-patterns/ak47"
DECODE_KEY = b"op.gg-cs2-spray-2025"


def fetch_page(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def next_flight_stream(html):
    chunks = []
    pattern = r'self\.__next_f\.push\(\[1,"(.*?)"\]\)</script>'
    for match in re.finditer(pattern, html, re.S):
        chunks.append(json.loads('"' + match.group(1) + '"'))
    return "".join(chunks)


def extract_text_record(stream, record_id):
    match = re.search(rf"{re.escape(record_id)}:T([0-9a-fA-F]+),", stream)
    if not match:
        raise ValueError(f"Could not find React Flight text record {record_id}.")

    length = int(match.group(1), 16)
    start = match.end()
    return stream[start : start + length]


def extract_braced_json(stream, label):
    label_index = stream.find(label)
    if label_index == -1:
        raise ValueError(f"Could not find {label}.")

    start = stream.find("{", label_index)
    depth = 0
    in_string = False
    escaped = False

    for index, character in enumerate(stream[start:], start):
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue

        if character == '"':
            in_string = True
        elif character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth == 0:
                return json.loads(stream[start : index + 1])

    raise ValueError(f"Could not parse {label}.")


def decode_patterns(encoded):
    raw = base64.b64decode(encoded)
    decoded = bytes(byte ^ DECODE_KEY[index % len(DECODE_KEY)] for index, byte in enumerate(raw))
    return json.loads(decoded.decode("utf-8"))


def to_toolbox_pattern(weapon_id, source_pattern, weapon_info):
    info = weapon_info.get(weapon_id, {})
    interval_ms = info.get("intervalMs", 100)
    source_points = source_pattern.get("pattern", [])

    points = []
    for index, point in enumerate(source_points):
        points.append(
            {
                # OP.GG flips x when drawing the spray pattern. Store that orientation here.
                "x": round(-float(point["x"]), 4),
                "y": round(float(point["y"]), 4),
                "time": round(index * interval_ms / 1000, 4),
                "bullet": int(point.get("shot", index + 1)),
                "samples": int(point.get("samples", 0)),
            }
        )

    return {
        "id": "weapon_" + weapon_id,
        "name": info.get("name", source_pattern.get("weapon", weapon_id)),
        "clipSize": int(source_pattern.get("max_shots") or len(points)),
        "cycleTime": round(interval_ms / 1000, 4),
        "intervalMs": interval_ms,
        "source": "OP.GG CS2 Spray Patterns",
        "sourceUrl": f"https://op.gg/cs2/spray-patterns/{weapon_id}",
        "points": points,
    }


def main():
    html = fetch_page(SOURCE_URL)
    stream = next_flight_stream(html)
    encoded = extract_text_record(stream, "3c")
    opgg_patterns = decode_patterns(encoded)
    weapon_info = extract_braced_json(stream, '"weaponInfo":')

    patterns = [
        to_toolbox_pattern(weapon_id, opgg_patterns[weapon_id], weapon_info)
        for weapon_id in sorted(opgg_patterns)
    ]
    patterns.sort(key=lambda pattern: pattern["name"])

    output = {
        "source": "https://op.gg/cs2/spray-patterns/ak47",
        "note": "Decoded from OP.GG's client payload. Check OP.GG terms before republishing this dataset.",
        "patterns": patterns,
    }
    OUTPUT_PATH.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"wrote {len(patterns)} patterns to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
