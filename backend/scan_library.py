import os
import json
from pathlib import Path
from mutagen import File
from mutagen.id3 import ID3, ID3NoHeaderError
from tqdm import tqdm

SUPPORTED_EXTENSIONS = ('.mp3', '.flac', '.m4a', '.wav', '.aiff', '.aif', '.ogg')

def extract_metadata(file_path):
    audio = File(str(file_path), easy=True)

    metadata = {
        'path': str(file_path),
        'title': None,
        'artist': None,
        'album': None,
        'genre': None,
        'date': None,
        'tracknumber': None,
    }

    if audio:
        metadata.update({
            'title': audio.get('title', [None])[0],
            'artist': audio.get('artist', [None])[0],
            'album': audio.get('album', [None])[0],
            'genre': audio.get('genre', [None])[0],
            'date': audio.get('date', [None])[0],
            'tracknumber': audio.get('tracknumber', [None])[0],
        })

    # Fallback for AIFF/ID3 tags
    if file_path.suffix.lower() in ['.aiff', '.aif']:
        try:
            id3 = ID3(str(file_path))
            metadata['title'] = metadata['title'] or getattr(id3.get("TIT2", None), "text", [None])[0]
            metadata['artist'] = metadata['artist'] or getattr(id3.get("TPE1", None), "text", [None])[0]
            metadata['album'] = metadata['album'] or getattr(id3.get("TALB", None), "text", [None])[0]
            metadata['genre'] = metadata['genre'] or getattr(id3.get("TCON", None), "text", [None])[0]
            metadata['date'] = metadata['date'] or getattr(id3.get("TDRC", None), "text", [None])[0]
            metadata['tracknumber'] = metadata['tracknumber'] or getattr(id3.get("TRCK", None), "text", [None])[0]
        except ID3NoHeaderError:
            pass  # No ID3 header, continue

    return metadata

def scan_music_folder(root_dir: Path):
    music_data = []
    file_paths = []

    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.lower().endswith(SUPPORTED_EXTENSIONS):
                file_paths.append(Path(dirpath) / file)

    for file_path in tqdm(file_paths, desc="📦 Scanning files"):
        try:
            meta = extract_metadata(file_path)
            music_data.append(meta)
        except Exception as e:
            print(f"⚠️ Skipping {file_path.name} due to error: {e}")
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
