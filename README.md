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
  - Get star ratings and other rekordbox specific metadata

- Youtube track previews:
  - On tile hover, show play button
  - On play click, show YouTube player in hovering window in lower RH corner
  - Get full youtube links (python backend --> get_yt_link(artist, title, length?)
  - Generate playlists: After the selected track finishes, play a nearby track (generate playlists by proximity on canvas -- x,y coords)

- Display modes:
  - Navigation menu to switch views? Canvas or list
  - Album art - on tiles or popup?
  - Playlists: python backend -> read in .m3u (or similar) files and use these to create islands
  - 2D canvas view:
    - Should placement calculations happen in frontend? probably, so that user can create views via the UI (e.g., use a filter to create a subset then select display setting like 2D canvas + hex) 
    - Hex islands: fix spacing (tiles closer together)
    - Rectangular/square islands
    - Search/filtering
    - Genre relations? Place similar genres closer together
    - Venn diagram style -- set 'genre centres' and then place track tile with equal proximity to each relevant centre? weighting based on primary, secondary, tertiary?? 
  - File list view with sorting/search/filtering (like rekordbox collection view) -- file structure tree view?? use List.js

- General UI:
  - Title Bar: display file library name, name of current view (e.g., all songs, grouped by primary genre into hex islands) date created and some stats?
  - Favicon? low priority
  - Mobile UI: pinch to zoom, click to select, improve panning?
  - Create 'liked' playlist (on hover, show heart icon, on click add to list in sidebar?) -- option to export as text? or youtube playlist?
 
- Performance: test with a larger library (e.g., 2000 tracks?)
  - Is dynamic loading/chunking needed to avoid lags? limit zoom out and then only load tiles within view?
  - What is file size for prepared.json when library of this size is loaded?

- At some point:
  - Handle Discogs collection/wantlist export (.csv)
  - Handle other music management software exports (serato, engine, itunes)
  - Bandcamp collection/wantlist exports: https://github.com/dbeley/bandcamp-library-scraper
  - Streaming libraries?? 

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

