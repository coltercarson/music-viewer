# music-viewer
Tools for displaying local music library on a webpage.

Background/ideas: https://docs.google.com/document/d/1xcNdlIfbqIN5MVHyVnceiRLx-8G4bPj5zbAf5KZB12s/edit?usp=sharing

# Notes:
install node.js at https://nodejs.org/en/download

# Planned features:
- File scanning:
  - Get track length
 
- Handle rekordbox.yml files:
  - Generate prepared.json from rekordbox library instead of file scan

- Track previews:
  - On tile hover, show play button
  - On play click, show YouTube player in hovering window in lower RH corner
  - Get full youtube links (python backend --> get_yt_link(artist, title, length?)
  - Generate playlists: After the selected track finishes, play a nearby track (generate playlists by proximity on canvas -- x,y coords)

- Display modes:
  - Navigation menu to switch views?
  - 2D canvas view:
    - Hex islands: fix spacing (tiles closer together)
    - Rectangular/square islands
    - Search/filtering UI
  - List view with sorting/search/filtering
  - File structure tree view??
    
- General UI:
  - Title Bar: display file library name, date created and some stats?
  - Favicon? low priority

- Performance: test with a larger library (e.g., 2000 tracks?)
  - Is dynamic loading/chunking needed to avoid lags?
  - What is file size for prepared.json when library of this size is loaded?

## Frontend

The frontend React app lives in `/frontend`.

To run it:

```bash
cd frontend
npm install
npm run dev
```

### Package

prepared.json file is copied from backend (data/json) to front end by predev line

