import React, { useRef, useState, useEffect } from "react";
import YouTube from 'react-youtube';
import { Stage, Layer } from "react-konva";
import TrackTile from "./components/TrackTile";
import TrackDetails from "./components/TrackDetails";

export default function App() {
  const stageRef = useRef(null);
  const [scale, setScale] = useState(1);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [tracks, setTracks] = useState([]);
  const [selectedTrack, setSelectedTrack] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [currentPreviewTrackId, setCurrentPreviewTrackId] = useState(null);

  useEffect(() => {
    fetch(import.meta.env.BASE_URL + "prepared.json")
      .then((res) => res.json())
      .then((data) => {
        console.log("Loaded tracks:", data);
        setTracks(data);
      });
  }, []);

  const handleWheel = (e) => {
    e.evt.preventDefault();
    const stage = stageRef.current;
    const oldScale = stage.scaleX();
    const pointer = stage.getPointerPosition();
    const mousePointTo = {
      x: (pointer.x - stage.x()) / oldScale,
      y: (pointer.y - stage.y()) / oldScale,
    };
    const scaleBy = 1.1;
    const newScale = e.evt.deltaY > 0 ? oldScale / scaleBy : oldScale * scaleBy;
    setScale(newScale);
    setPosition({
      x: pointer.x - mousePointTo.x * newScale,
      y: pointer.y - mousePointTo.y * newScale,
    });
  };

  function extractYouTubeId(url) {
    try {
      const urlObj = new URL(url);
      if (urlObj.hostname === 'youtu.be') {
        return urlObj.pathname.slice(1);
      } else if (urlObj.hostname.includes('youtube.com')) {
        return urlObj.searchParams.get('v');
      }
    } catch (e) {
      console.warn('Invalid YouTube URL:', url);
      return null;
    }
  }
  
  function handlePreviewEnded() {
    const currentIndex = tracks.findIndex(t => t.id === currentPreviewTrackId);
    const nextTrack = tracks[currentIndex + 1];

    if (nextTrack && nextTrack.preview_url) {
      setCurrentPreviewTrackId(nextTrack.id);
      setPreviewUrl(nextTrack.preview_url);
    } else {
      setCurrentPreviewTrackId(null);
      setPreviewUrl(null); // No more previews to play
    }
  }

  return (
    <>
      <Stage
        width={window.innerWidth}
        height={window.innerHeight}
        onWheel={handleWheel}
        scaleX={scale}
        scaleY={scale}
        x={position.x}
        y={position.y}
        draggable
        ref={stageRef}
      >
        <Layer>
          {tracks.map((track, i) => (
            <TrackTile
              key={i}
              track={track}
              x={(i % 10) * 150}
              y={Math.floor(i / 10) * 150}
              onClick={() => setSelectedTrack(track)}
              onPlayClick={(url, id) => {
                setCurrentPreviewTrackId(id);
                setPreviewUrl(url);
              }}
            />
          ))}
        </Layer>
      </Stage>

      {selectedTrack && (
        <TrackDetails track={selectedTrack} onClose={() => setSelectedTrack(null)} />
      )}

      {previewUrl && (
        <div
          style={{
            position: "fixed",
            bottom: 20,
            right: 20,
            width: "320px",
            height: "180px",
            zIndex: 1000,
            backgroundColor: "black",
            borderRadius: "8px",
            overflow: "hidden",
            boxShadow: "0 4px 12px rgba(0,0,0,0.3)",
          }}
        >
          <YouTube
            videoId={extractYouTubeId(previewUrl)}
            opts={{
              width: "100%",
              height: "100%",
              playerVars: {
                autoplay: 1,
              },
            }}
            onEnd={handlePreviewEnded} // ✅ called when video ends
          />

          <button
            onClick={() => {
              setPreviewUrl(null);
              setCurrentPreviewTrackId(null);
            }}
            style={{
              position: "absolute",
              top: 5,
              right: 5,
              background: "rgba(0,0,0,0.6)",
              border: "none",
              color: "white",
              padding: "2px 6px",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            ✕
          </button>
        </div>
      )}


    </>
  );
}
