import React, { useRef, useState, useEffect } from "react";
import { Stage, Layer } from "react-konva";
import TrackTile from "./components/TrackTile";
import TrackDetails from "./components/TrackDetails";

export default function App() {
  const stageRef = useRef(null);
  const [scale, setScale] = useState(1);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [tracks, setTracks] = useState([]);
  const [selectedTrack, setSelectedTrack] = useState(null);

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
            />
          ))}
        </Layer>
      </Stage>

      {selectedTrack && (
        <TrackDetails track={selectedTrack} onClose={() => setSelectedTrack(null)} />
      )}
    </>
  );
}
