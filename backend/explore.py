
import math
from pathlib import Path
import json
import hashlib
from collections import defaultdict
from plot import check_layout
import os

from prepare_metadata import *
from plot import *
from scan_library import scan_library


# base_dir = Path(__file__).resolve().parents[1]
# input_json = base_dir / "data" / "json" / "output.json"
# output_json = base_dir / "frontend" / "public" / "prepared.json"

# 
# with input_json.open("r", encoding="utf-8") as f:
#     raw_tracks = json.load(f)

# # Filter out tracks with no genre
# raw_tracks = [track for track in raw_tracks if track.get("genre") is not None]

# genre_groups = get_genre_groups(raw_tracks)

# 

# islands_db = build_islands_db(genre_groups)

# prepared_tracks = []

# island = islands_db[2]

# track = island.tracks[0]


base_dir = Path(__file__).resolve().parents[1]

# music_dir = Path(r'f:\DJ MUSIC\DEEMIX')
# music_dir = base_dir / "data" / "music"
# output_path = base_dir / "data" / "json" / "output.json"
# scan_library(music_dir, output_path)

scan_library(
    rekordbox_xml_path=Path(r"F:/250701_T7.xml"),
    playlist_name="5STAR_ALL",
    output_path=Path(os.path.join(base_dir, "data/json/rekordbox_5star.json"))
)

input_json = base_dir / "data" / "json" / "rekordbox_5star.json"
output_json = base_dir / "frontend" / "public" / "prepared.json"
main(input_json, output_json)
# check_layout()  # Optional: visualize the layout after preparation


# Check island circles
# radii = [island_radius(len(tracks)) for tracks in genre_groups.values()]
# centres = island_centres(radii)
# plot_island_circles(radii, centres)

