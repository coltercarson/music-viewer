# imports
import math
from pathlib import Path
import json
import hashlib
from collections import defaultdict
from typing import List, Tuple, Literal
from tqdm import tqdm
from youtubesearchpython import VideosSearch

from plot import check_layout
from youtube import get_youtube_url

# constants

config_path = Path(__file__).parent.parent / "config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

secrets_path = Path(__file__).parent.parent / "data" / "secrets.json"
with open(secrets_path, "r", encoding="utf-8") as f:
    secrets = json.load(f)

TILE_SIZE = config.get("tileSize")
INNER_GAP = config.get("tileGap")
ISLAND_GAP = config.get("islandGap")
CENTRE_X = config.get("centreX")
CENTRE_Y = config.get("centreY")

# CLEAN
def clean_genre(genre):
    if not genre:
        return "unknown"
    return [g.strip() for g in genre.split(",") if g.strip()]

# GENERATE NEW DATA
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

def get_genre_colour(genre, genre_groups):
    # Assign a unique primary colour to each genre, cycling if needed
    primary_colours = [
        "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
        "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe",
        "#008080", "#e6beff", "#9a6324", "#fffac8", "#800000",
        "#aaffc3", "#808000", "#ffd8b1", "#000075", "#808080"
    ]
    genre_list = sorted(genre_groups.keys())
    colour_map = {g: primary_colours[i % len(primary_colours)] for i, g in enumerate(genre_list)}
    return colour_map.get(genre, "#cccccc")

def get_genre_groups(tracks: list) -> defaultdict:
    """
    Groups a list of track dictionaries by their cleaned and normalized genre names.

    Args:
        tracks (list of dict): A list of track dictionaries, each containing at least a "genre" key.

    Returns:
        defaultdict: A dictionary where keys are cleaned genre names and values are lists of tracks belonging to each genre.

    Note:
        This function relies on an external `clean_genre` function to process genre names.
    """

    genre_groups = defaultdict(list)
    for track in tracks:
        genre = clean_genre(track.get("genre"))
        primary_genre = genre[0] if isinstance(genre, list) else genre
        genre_groups[primary_genre].append(track)
    return genre_groups


# LAYOUT

def island_radius(n: int, tile_sz: float = 100.0, gap: float = 10.0) -> float:
    """
    Returns the radius (pixels) needed to fit `n` square tiles
    on a compact hex-style grid.
      * `tile_sz` – tile width/height in px
      * `gap`     – clear space between tile edges in px
    """
    if n < 1:
        raise ValueError("Number of tiles must be ≥ 1")
    if n == 1:
        return tile_sz / 2 # just the single tile

    # How many hexagonal rings are required?
    # Perfect hex with R rings holds 1 + 3R(R+1) tiles.
    R = math.ceil((math.sqrt(12 * n - 3) - 3) / 6)

    pitch = tile_sz + gap # centre-to-centre spacing
    return pitch * R * math.sqrt(3) + tile_sz / 2

def _hex_rings_needed(n: int) -> int:
    """
    Helper for island_tile_positions():
    Rings required to hold n tiles  ⇒  R
    Perfect hex with R rings: N = 1 + 3 R (R+1)
    """
    if n <= 1:
        return 0
    return math.ceil((math.sqrt(12 * n - 3) - 3) / 6)

_ROOT3 = math.sqrt(3)
def _axial_to_cart(
    q: int,
    r: int,
    pitch: float,
    orientation: Literal["pointy", "flat"] = "pointy"
) -> Tuple[float, float]:
    """
    Convert axial hex-grid coordinates (q, r) → Cartesian (x, y).

    Parameters
    ----------
    q, r        : axial coordinates
    pitch       : centre-to-centre distance between adjacent hexes
                  (use tile_size + gap for your square “tiles”)
    orientation : "pointy" | "flat"
                  • "pointy"  → hexes have a vertex at the top (default)
                  • "flat"    → hexes have a flat edge at the top

    Returns
    -------
    (x, y) tuple giving canvas coordinates for the hex (or square tile).
    """
    if orientation == "pointy":
        # classic axial layout with vertical columns
        x = pitch * (1.5 * q)
        y = pitch * (_ROOT3 / 2 * q + _ROOT3 * r)
    elif orientation == "flat":
        # 90°-rotated layout with horizontal rows
        x = pitch * (_ROOT3 * q + _ROOT3 / 2 * r)
        y = pitch * (1.5 * r)
    else:
        raise ValueError("orientation must be 'pointy' or 'flat'")

    return x, y


def island_tile_positions(n: int,
                     centre: Tuple[float, float] = (CENTRE_X, CENTRE_Y),
                     tile_sz: float = TILE_SIZE,
                     gap: float = INNER_GAP) -> List[Tuple[float, float]]:
    """
    Return a list of (x, y) centres for `n` square tiles arranged
    compactly around `centre` on a hex/brick grid.

    Args
    ----
    n        : number of tiles (≥1)
    centre   : (cx, cy) of the island’s centre
    tile_sz  : tile width/height in pixels
    gap      : clearance between tile edges in pixels

    Example
    -------
    >>> coords = island_positions(7, centre=(400, 300))
    """
    if n < 1:
        raise ValueError("Number of tiles must be ≥ 1")

    cx, cy   = centre
    pitch    = tile_sz + gap          # centre-to-centre spacing
    rings    = _hex_rings_needed(n)   # how many layers we’ll need
    coords   = [(cx, cy)]             # tile 0 at the exact centre

    if n == 1:
        return coords

    # Directions around a hex in axial coordinates
    DIRECTIONS = [(1, 0), (1, -1), (0, -1),
                  (-1, 0), (-1, 1), (0, 1)]

    tiles_placed = 1
    # Walk rings 1 … R
    for r in range(1, rings + 1):
        q, s = -r, r                  # start at “west” corner (-r, +r)
        for dir_q, dir_s in DIRECTIONS:
            steps = r                 # how many tiles along this edge
            for _ in range(steps):
                if tiles_placed >= n:
                    return coords
                # axial → cartesian → shift to island centre
                dx, dy = _axial_to_cart(q, s, pitch)
                coords.append((cx + dx, cy + dy))
                tiles_placed += 1
                q += dir_q
                s += dir_s

    return coords




def _dist(p: Tuple[float, float], q: Tuple[float, float]) -> float:
    """Helper for island_centres(): distance and circle–circle intersection"""
    return math.hypot(p[0] - q[0], p[1] - q[1])

def _circle_intersections(c0, r0, c1, r1) -> List[Tuple[float, float]]:
    """
    Return up to two intersection points of circles
    (c0, r0) and (c1, r1).  Empty list if no intersection.
    """
    x0, y0 = c0
    x1, y1 = c1
    d = _dist(c0, c1)
    if d == 0 or d > r0 + r1 or d < abs(r0 - r1):
        return []

    # Distance from c0 to the line between the two intersections
    a = (r0**2 - r1**2 + d**2) / (2 * d)
    h_sq = r0**2 - a**2
    if h_sq < 0:                       # numeric noise
        return []
    h = math.sqrt(h_sq)

    # Base point P2 along the line c0→c1
    x2 = x0 + a * (x1 - x0) / d
    y2 = y0 + a * (y1 - y0) / d

    # Offset vector perpendicular to c0→c1
    rx = -(y1 - y0) * (h / d)
    ry =  (x1 - x0) * (h / d)

    return [(x2 + rx, y2 + ry), (x2 - rx, y2 - ry)]


def island_centres(
    radii: List[float],
    centre: Tuple[float, float] = (CENTRE_X, CENTRE_Y),
    island_gap: float = ISLAND_GAP
) -> List[Tuple[float, float]]:
    """
    Compute (x, y) centres for islands treated as non-overlapping circles.

    Parameters
    ----------
    radii       : list of island radii (edge of tiles → centre distance)
    centre      : fixed position of the first island (usually canvas centre)
    island_gap  : minimum clearance *between edges* of any two islands

    Returns
    -------
    centres : list[(x, y)] corresponding to the input order in *radii*
    """
    if not radii:
        return []

    # First island is anchored at the given centre
    centres: List[Tuple[float, float]] = [centre]

    for i in range(1, len(radii)):
        r_new = radii[i]
        best_pos = None
        best_dist = float("inf")

        # Convenience: augmented radii include mandatory gap
        aug = [r + r_new + island_gap for r in radii[:i]]

        # Candidates tangential to *one* existing island
        for (cx, cy), aug_r in zip(centres, aug):
            # Project along line centre→(cx, cy) inward toward the hub
            vx, vy = centre[0] - cx, centre[1] - cy
            v_len = math.hypot(vx, vy)
            if v_len == 0:
                # Existing island *is* the hub; skip – circle touch will
                # be handled by two-circle candidates anyway
                continue
            scale = aug_r / v_len
            cand = (cx + vx * scale, cy + vy * scale)

            if _valid(cand, r_new, centres, radii[:i], island_gap):
                d = _dist(cand, centre)
                if d < best_dist:
                    best_dist, best_pos = d, cand

        # Candidates tangential to *two* existing islands
        n_prev = len(centres)
        for j in range(n_prev):
            for k in range(j + 1, n_prev):
                cA, cB = centres[j], centres[k]
                rA, rB = aug[j], aug[k]

                for cand in _circle_intersections(cA, rA, cB, rB):
                    if _valid(cand, r_new, centres, radii[:i], island_gap):
                        d = _dist(cand, centre)
                        if d < best_dist:
                            best_dist, best_pos = d, cand
                            
        # Fallback — should rarely happen
        if best_pos is None:
            # Place on a ray to the right, just outside outermost ring
            max_r = max(_dist(c, centre) + radii[j]
                        for j, c in enumerate(centres))
            best_pos = (centre[0] + max_r + r_new + island_gap, centre[1])

        centres.append(best_pos)

    return centres

def _valid(cand, r_new, centres, radii_so_far, gap) -> bool:
    """
    Helper for island_centres(): overlap / clearance test
    True if `cand` is clear of all existing islands by at least `gap`.
    """
    for (px, py), r_old in zip(centres, radii_so_far):
        if _dist(cand, (px, py)) < r_new + r_old + gap - 1e-6:
            return False
    return True

class Island:
    def __init__(
        self,
        radius: float,
        tile_positions: list,
        centre: tuple,
        colour: str,
        tracks: list,
        genre: str, 
    ):
        self.radius = radius
        self.tile_positions = tile_positions  # List of (x, y) for each tile
        self.centre = centre                  # (x, y) of island centre
        self.colour = colour                  # Colour string (e.g. "#e6194b")
        self.tracks = tracks                  # List of track dicts
        self.genre = genre                  # List of track dicts

    def __repr__(self):
        return (
            f"Island(radius={self.radius}, centre={self.centre}, "
            f"tiles={len(self.tile_positions)}, colour={self.colour}, "
            f"genre={self.genre}, "
            f"tracks={len(self.tracks)})"
        )

def build_islands_db(genre_groups: defaultdict) -> List[Island]:
    """
    Build a list of Island objects from genre groups.
    
    Args:
        genre_groups (defaultdict): Dictionary where keys are genres and values are lists of tracks.
    
    Returns:
        List[Island]: List of Island objects with their properties set.
    """
    islands = []
    radii = [island_radius(len(tracks)) for tracks in genre_groups.values()]
    centres = island_centres(radii, centre=(CENTRE_X, CENTRE_Y), island_gap=ISLAND_GAP)
    tile_positions = [island_tile_positions(len(tracks), centre, TILE_SIZE, INNER_GAP) for tracks, centre in zip(genre_groups.values(), centres)]
    
    assert len(radii) == len(centres) == len(tile_positions) == len(genre_groups), "Mismatch in number of radii, centres, and tile positions"

    for (genre, tracks), (radius, centre, positions) in zip(genre_groups.items(), zip(radii, centres, tile_positions)):
        colour = get_genre_colour(genre, genre_groups)
        island = Island(radius, positions, centre, colour, tracks, genre)
        islands.append(island)
    
    return islands

# MAIN FUNCTION
def main(input_json: Path, output_json: Path):
    with input_json.open("r", encoding="utf-8") as f:
        raw_tracks = json.load(f)

    # Filter out tracks with no genre
    # raw_tracks = [track for track in raw_tracks if track.get("genre") is not None]

    genre_groups = get_genre_groups(raw_tracks)

    islands_db = build_islands_db(genre_groups)

    prepared_tracks = []

    for island in tqdm(islands_db, desc="Processing islands"):
        for i, track in enumerate(tqdm(island.tracks, desc=f"Tracks in {island.genre}", leave=False)):
            decade = estimate_decade(track.get("date"))
            youtube_url = get_youtube_url(track) if track.get("artist") and track.get("title") else None
            prepared = {
                "id": generate_id(track),
                "title": track.get("title", "Unknown Title"),
                "artist": track.get("artist", "Unknown Artist"),
                "album": track.get("album", ""),
                "genre": track.get("genre"),
                "decade": decade,
                "date": track.get("date"),
                "tracknumber": track.get("tracknumber"),
                "path": track.get("path"),
                "x": round(island.tile_positions[i][0], 2),
                "y": round(island.tile_positions[i][1], 2),
                "colour": island.colour,
                "preview_url": youtube_url,
                "buy_url": f"https://bandcamp.com/search?q={track.get('artist', '')}+{track.get('title', '')}".replace(" ", "+"),
            }
            prepared_tracks.append(prepared)

    output_json.parent.mkdir(parents=True, exist_ok=True)
    with output_json.open("w", encoding="utf-8") as f:
        json.dump(prepared_tracks, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[1]
    input_json = base_dir / "data" / "json" / "output.json"
    output_json = base_dir / "frontend" / "public" / "prepared.json"

    main(input_json, output_json)
    print(f"✅ Metadata prepared and saved to {output_json}")
    # check_layout()  # Optional: visualize the layout after preparation
    # print("✅ Layout checked.")
    # print("Done.")

