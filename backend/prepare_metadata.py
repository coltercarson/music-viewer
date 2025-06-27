import json
import hashlib
import random
from pathlib import Path

# Define genre → x and decade → y mappings
GENRE_X = {
    'cosmic disco': 100, 'electronic': 200, 'drum & bass': 300,
    'techno': 400, 'house': 500, 'ambient': 600, 'jazz': 700,
}
DECADE_Y = {
    '1990s': 100, '2000s': 200, '2010s': 300, '2020s': 400,
}

def clean_genre(genre):
    if not genre:
        return "unknown"
    return genre.lower().split(',')[0].split(';')[0].strip()

def estimate_decade(date_str):
    if not date_str or not any(c.isdigit() for c in date_str):
        return "unknown"
    try:
        year = int(date_str[:4])
        return f"{year // 10 * 10}s"
    except:
        return "unknown"

def generate_id(track):
    base = (track.get("path") or "") + (track.get("title") or "")
    return hashlib.md5(base.encode("utf-8")).hexdigest()

def prepare_metadata(input_path: Path, output_path: Path):
    with input_path.open("r", encoding="utf-8") as f:
        raw_tracks = json.load(f)

    prepared_tracks = []
    for track in raw_tracks:
        genre = clean_genre(track.get("genre"))
        decade = estimate_decade(track.get("date"))

        x = GENRE_X.get(genre, random.randint(0, 1000)) + random.randint(-20, 20)
        y = DECADE_Y.get(decade, random.randint(0, 1000)) + random.randint(-20, 20)

        prepared = {
            "id": generate_id(track),
            "title": track.get("title", "Unknown Title"),
            "artist": track.get("artist", "Unknown Artist"),
            "album": track.get("album", ""),
            "genre": genre,
            "decade": decade,
            "date": track.get("date"),
            "tracknumber": track.get("tracknumber"),
            "path": track.get("path"),
            "x": x,
            "y": y,
            # "search_text": " ".join([
            #     track.get("title", ""),
            #     track.get("artist", ""),
            #     genre,
            #     decade,
            # ]).lower(),
            "preview_url": f"https://www.youtube.com/results?search_query={track.get('artist', '')}+{track.get('title', '')}".replace(" ", "+")
        }

        prepared_tracks.append(prepared)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(prepared_tracks, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[1]
    input_json = base_dir / "data" / "json" / "output.json"
    output_json = base_dir / "data" / "json" / "prepared.json"

    prepare_metadata(input_json, output_json)
    print(f"✅ Metadata prepared and saved to {output_json}")
