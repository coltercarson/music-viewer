import React from 'react';
import { Rect, Text, Group } from "react-konva";
import config from '../../../config.json';

export default function TrackTile({ track, onClick }) {
  const size = config.tileSize;

  return (
    <Group x={track.x} y={track.y} onClick={onClick}>
      <Rect
        width={size}
        height={size}
        fill={track.colour || "lightblue"}
        stroke="black"
        strokeWidth={2}
        cornerRadius={1}
      />
      <Text
        text={`${track.artist}\n${track.title}\nGenre: ${track.genre}`}
        fontSize={10}
        padding={8}
        width={size}
        height={size}
        fill="black"
        wrap="word"
      />
    </Group>
  );
}
