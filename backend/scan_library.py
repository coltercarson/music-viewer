import os
import json
from pathlib import Path
from mutagen import File
from tqdm import tqdm

SUPPORTED_EXTENSIONS = ('.mp3', '.flac', '.m4a', '.wav', '.aiff', '.aif', '.ogg')

def scan_music_folder(root_dir: Path):
    music_data = []
    file_paths = []

    # Collect all supported files
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.lower().endswith(SUPPORTED_EXTENSIONS):
                file_paths.append(Path(dirpath) / file)

    # Process with progress bar
    for file_path in tqdm(file_paths, desc="📦 Scanning files"):
        try:
            audio = File(str(file_path), easy=True)  # Ensure str path is passed
            if audio:
                track_data = {
                    'path': str(file_path),
                    'title': audio.get('title', [None])[0],
                    'artist': audio.get('artist', [None])[0],
                    'album': audio.get('album', [None])[0],
                    'genre': audio.get('genre', [None])[0],
                    'date': audio.get('date', [None])[0],
                    'tracknumber': audio.get('tracknumber', [None])[0],
                }
                music_data.append(track_data)
        except Exception as e:
            print(f"⚠️ Skipping {file_path} due to error: {e}")
    return music_data

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[1]
    music_dir = base_dir / "data" / "music"
    output_path = base_dir / "data" / "json" / "output.json"

    print(f"🔍 Scanning music folder: {music_dir}")
    collection = scan_music_folder(music_dir)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(collection, f, indent=2, ensure_ascii=False)

    print(f"✅ Metadata extracted and saved to {output_path}")
