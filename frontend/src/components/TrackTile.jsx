import React from 'react';
import { Rect, Text, Group } from "react-konva";

export default function TrackTile({ track, onClick }) {
  const size = 100;

  return (
    <Group x={track.x} y={track.y} onClick={onClick}>
      <Rect
        width={size}
        height={size}
        fill={track.colour || "lightblue"} // Use track colour or default
        stroke="black"
        strokeWidth={2}
        cornerRadius={1}
      />
      <Text
        text={`${track.artist}\n${track.title}\n${track.genre}`}
        fontSize={12}
        padding={8}
        width={size}
        height={size}
        fill="black"
        wrap="word"
      />
    </Group>
  );
}
